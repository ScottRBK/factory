import { lstat, realpath } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, isAbsolute, join } from "node:path";
import { getPackageDir, VERSION } from "@earendil-works/pi-coding-agent";
import { readBoundedJson } from "../adapters/local/bounded-json.ts";
import { ManagedPlanningPreferences } from "../adapters/local/planning-settings.ts";
import type {
  ForgetfulConfig,
  ModelSelection,
} from "../config.ts";
import {
  DEFAULT_FORGETFUL_RECALL_MODEL_TIMEOUT_MS,
  DEFAULT_FORGETFUL_TIMEOUT_MS,
  DEFAULT_MEMORY_CONTEXT_LIMIT_TOKENS,
  DEFAULT_RECALL_CONCURRENCY,
  DEFAULT_RECALL_DEADLINE_MS,
} from "../config.ts";
import {
  createForgetfulExtension,
  type ForgetfulExtensionOptions,
} from "../extension.ts";

const SUPPORTED_PI_VERSION = "1.4.0";
const SUPPORTED_UNDICI_VERSION = "8.12.2";
const TOKEN_ENV_NAME = /^[A-Za-z_]\w*$/;
const MODEL_NAME = /^([^/\s]+)\/(.+)$/;
const SUPPORTED_RUNTIME = "Supported managed runtime requires Pi 1.4.0, host Undici 8.12.2, " +
  "and the standard HTTP/1 parser.";

type JsonObject = Record<string, unknown>;

interface ManagedPreferences {
  enabled: boolean;
  capture_mode: "auto" | "off";
  model: string | null;
}

function object(value: unknown, label: string): JsonObject {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be a JSON object.`);
  }
  return value as JsonObject;
}

function exactKeys(value: JsonObject, expected: string[], label: string): void {
  const keys = Object.keys(value).sort((left, right) => left.localeCompare(right));
  const wanted = [...expected].sort((left, right) => left.localeCompare(right));
  if (keys.length !== wanted.length || keys.some((key, index) => key !== wanted[index])) {
    throw new Error(`${label} must contain exactly: ${wanted.join(", ")}.`);
  }
}

async function verifyManagedRuntime(env: NodeJS.ProcessEnv): Promise<void> {
  if (env.PI_PACKAGE_DIR !== undefined) {
    throw new Error(`${SUPPORTED_RUNTIME} PI_PACKAGE_DIR is not supported in managed mode.`);
  }
  if (VERSION !== SUPPORTED_PI_VERSION) {
    throw new Error(`${SUPPORTED_RUNTIME} Detected Pi ${VERSION}.`);
  }
  if (env.UNDICI_USE_MILO === "1" || env.UNDICI_USE_MILO === "true") {
    throw new Error(`${SUPPORTED_RUNTIME} The experimental parser is enabled.`);
  }
  let metadata: JsonObject;
  try {
    const hostRequire = createRequire(join(getPackageDir(), "package.json"));
    const path = hostRequire.resolve("undici/package.json");
    metadata = object(await readBoundedJson(path, "Host Undici package metadata"),
      "Host Undici package metadata");
  } catch {
    throw new Error(`${SUPPORTED_RUNTIME} Host Undici metadata could not be verified.`);
  }
  if (metadata.version !== SUPPORTED_UNDICI_VERSION) {
    const detected = typeof metadata.version === "string" ? metadata.version : "unverified";
    throw new Error(`${SUPPORTED_RUNTIME} Detected host Undici ${detected}.`);
  }
}

function selectedModel(value: string | null): ModelSelection | undefined {
  if (value === null) return undefined;
  const match = MODEL_NAME.exec(value);
  const provider = match?.[1];
  const id = match?.[2];
  const trimmedId = id?.trim();
  if (!provider || !trimmedId || trimmedId !== id) {
    throw new Error("forgetful.json model must be provider/model or null.");
  }
  return { provider, id: trimmedId };
}

function preferences(value: unknown): ManagedPreferences {
  const data = object(value, "forgetful.json");
  exactKeys(data, ["enabled", "capture_mode", "model"], "forgetful.json");
  if (typeof data.enabled !== "boolean") {
    throw new TypeError("forgetful.json enabled must be boolean.");
  }
  if (data.capture_mode !== "auto" && data.capture_mode !== "off") {
    throw new Error("forgetful.json capture_mode must be auto or off.");
  }
  if (data.capture_mode !== (data.enabled ? "auto" : "off")) {
    throw new Error("forgetful.json capture_mode must agree with enabled.");
  }
  if (data.model !== null && typeof data.model !== "string") {
    throw new Error("forgetful.json model must be provider/model or null.");
  }
  if (data.enabled && data.model === null) {
    throw new Error("forgetful.json model is required when memory is enabled.");
  }
  selectedModel(data.model as string | null);
  return data as unknown as ManagedPreferences;
}

function restEndpoint(input: string): string {
  const url = new URL(input);
  if (!["http:", "https:"].includes(url.protocol) || url.username || url.password ||
      url.search || url.hash) {
    throw new Error("FORGETFUL_SERVER must be an HTTP(S) URL without credentials or query data.");
  }
  const path = url.pathname;
  if (path === "/") url.pathname = "/api/v1";
  else if (path.endsWith("/mcp")) url.pathname = `${path.slice(0, -4)}/api/v1`;
  else throw new Error("FORGETFUL_SERVER has an unsupported path; use root or terminal /mcp.");
  return url.toString().replace(/\/$/, "");
}

function positiveProjectId(value: string | undefined): number {
  if (!value || !/^[1-9]\d*$/.test(value)) {
    throw new Error("FACTORY_FORGETFUL_PROJECT_ID must be a positive project ID.");
  }
  const id = Number(value);
  if (!Number.isSafeInteger(id)) {
    throw new TypeError("FACTORY_FORGETFUL_PROJECT_ID must be a safe integer.");
  }
  return id;
}

async function managedToken(path: string, env: NodeJS.ProcessEnv): Promise<{
  token?: string;
  tokenEnv?: string;
}> {
  try {
    const data = object(await readBoundedJson(path, "forgetful-auth.json"),
      "forgetful-auth.json");
    exactKeys(data, ["token_env"], "forgetful-auth.json");
    if (typeof data.token_env !== "string" || !TOKEN_ENV_NAME.test(data.token_env)) {
      throw new Error("forgetful-auth.json token_env must name an environment variable.");
    }
    const token = env[data.token_env];
    if (!token) {
      throw new Error(`Configured token environment variable ${data.token_env} is not set.`);
    }
    return { token, tokenEnv: data.token_env };
  } catch (error) {
    if (error instanceof Error && "code" in error &&
        (error as NodeJS.ErrnoException).code === "ENOENT") return {};
    throw error;
  }
}

function unavailableConfig(
  status: "local" | "invalid",
  message: string,
  workspace = "",
): ForgetfulConfig {
  const stateRoot = workspace ? join(workspace, ".factory/data/pi-forgetful") : "";
  return {
    enabled: false,
    planningEnabled: false,
    planningPanel: false,
    captureMode: "off",
    verbosity: "warning",
    logging: "off",
    logDirectory: stateRoot ? join(stateRoot, "logs") : "",
    scope: "project",
    scopeSource: "project",
    instance: { baseUrl: "", timeoutMs: DEFAULT_FORGETFUL_TIMEOUT_MS },
    recallDeadlineMs: DEFAULT_RECALL_DEADLINE_MS,
    recallModelTimeoutMs: DEFAULT_FORGETFUL_RECALL_MODEL_TIMEOUT_MS,
    recallConcurrency: DEFAULT_RECALL_CONCURRENCY,
    contextLimitTokens: DEFAULT_MEMORY_CONTEXT_LIMIT_TOKENS,
    prompts: {},
    warnings: [message],
    managed: { status, message, workspace },
    queueRoot: stateRoot ? join(stateRoot, "queues") : undefined,
    paths: {
      userSettings: stateRoot ? join(stateRoot, "planning.json") : "",
      projectSettings: "",
    },
  };
}

async function loadManagedConfig(env: NodeJS.ProcessEnv): Promise<ForgetfulConfig> {
  const instance = env.FACTORY_FORGETFUL_INSTANCE;
  const workspaceInput = env.FACTORY_WORKSPACE;
  const agentFileInput = env.FACTORY_FOREMAN_AGENT_FILE;
  if (instance === "local") {
    const message = "Managed Foreman local memory is unavailable; " +
      "ordinary Factory CLI planning remains available.";
    return unavailableConfig("local", message, workspaceInput ?? "");
  }
  try {
    if (instance !== "server") {
      throw new Error("FACTORY_FORGETFUL_INSTANCE must select server mode.");
    }
    if (!workspaceInput || !agentFileInput || !isAbsolute(workspaceInput) ||
        !isAbsolute(agentFileInput)) {
      throw new Error("Factory workspace and Foreman agent file must be absolute paths.");
    }
    await verifyManagedRuntime(env);
    const workspace = workspaceInput;
    const agentFile = agentFileInput;
    const rootBefore = await lstat(agentFile);
    let definitionValue: unknown;
    if (!rootBefore.isSymbolicLink()) {
      definitionValue = await readBoundedJson(agentFile, "Foreman agent definition");
    } else {
      const target = await realpath(agentFile);
      definitionValue = await readBoundedJson(target, "Foreman agent definition");
      const rootAfter = await lstat(agentFile);
      const currentTarget = await realpath(agentFile);
      if (!rootAfter.isSymbolicLink() || rootBefore.dev !== rootAfter.dev ||
          rootBefore.ino !== rootAfter.ino || rootBefore.size !== rootAfter.size ||
          rootBefore.mtimeMs !== rootAfter.mtimeMs || rootBefore.ctimeMs !== rootAfter.ctimeMs ||
          currentTarget !== target) {
        throw new Error("Foreman agent definition selection changed while it was being read.");
      }
    }
    const definition = object(definitionValue, "Foreman agent definition");
    object(definition.agent, "Foreman agent definition agent");
    const directory = dirname(agentFile);
    const selected = preferences(await readBoundedJson(join(directory, "forgetful.json"),
      "forgetful.json"));
    const auth = await managedToken(join(directory, "forgetful-auth.json"), env);
    const projectId = positiveProjectId(env.FACTORY_FORGETFUL_PROJECT_ID);
    if (!env.FORGETFUL_SERVER) throw new Error("FORGETFUL_SERVER is required in server mode.");
    const baseUrl = restEndpoint(env.FORGETFUL_SERVER);
    const stateRoot = join(workspace, ".factory/data/pi-forgetful");
    const planningPath = join(stateRoot, "planning.json");
    const planningPanel = await new ManagedPlanningPreferences(planningPath, workspace).read();
    const status = selected.enabled ? "ready" : "memory-off";
    const message = selected.enabled
      ? `Managed Foreman memory uses fixed project #${projectId}.`
      : `Managed Foreman memory is off; planning uses fixed project #${projectId}.`;
    return {
      enabled: selected.enabled,
      planningEnabled: true,
      planningPanel,
      captureMode: selected.capture_mode,
      verbosity: "warning",
      logging: "off",
      logDirectory: join(stateRoot, "logs"),
      scope: "project",
      scopeSource: "project",
      instance: { baseUrl, ...auth, timeoutMs: DEFAULT_FORGETFUL_TIMEOUT_MS },
      recallDeadlineMs: DEFAULT_RECALL_DEADLINE_MS,
      recallModelTimeoutMs: DEFAULT_FORGETFUL_RECALL_MODEL_TIMEOUT_MS,
      recallConcurrency: DEFAULT_RECALL_CONCURRENCY,
      contextLimitTokens: DEFAULT_MEMORY_CONTEXT_LIMIT_TOKENS,
      model: selectedModel(selected.model),
      prompts: {},
      warnings: [],
      managed: { status, message, projectId, workspace },
      queueRoot: join(stateRoot, "queues"),
      paths: { userSettings: planningPath, projectSettings: "" },
    };
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    return unavailableConfig("invalid", `Managed Foreman memory is unavailable: ${reason}`,
      workspaceInput ?? "");
  }
}

export function createFactoryForgetfulExtension(
  options: Omit<ForgetfulExtensionOptions, "loadConfig" | "managed"> = {},
) {
  return createForgetfulExtension({
    ...options,
    managed: true,
    loadConfig: () => loadManagedConfig(process.env),
  });
}

