import json
from collections.abc import Callable
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.ports.foreman_terminal import ForemanTerminal
from forgetful_factory.application.ports.watch_lease import WatchLease
from forgetful_factory.application.scaffold_issue import ScaffoldIssue
from forgetful_factory.domain.models import FactoryError, Issue, WorkSource
from forgetful_factory.domain.services.work_tracking import WorkTrackingService


class WatchFactory:
    def __init__(self, tracking: WorkTrackingService, terminal: ForemanTerminal,
                 lease: WatchLease, scaffold: ScaffoldIssue):
        self.tracking = tracking
        self.terminal = terminal
        self.lease = lease
        self.scaffold = scaffold

    def run(self, config: FactoryConfiguration, workspace: Path, interval: float,
            choose_existing: Callable[[], bool], report: Callable[[str], None],
            report_error: Callable[[str], None]) -> None:
        with self.lease.hold():
            report('Checking Forgetful planning access; waiting for native sign-in/refresh if '
                   'needed. Browser OAuth may open; Ctrl-C cancels and preserves saved work.')
            self.scaffold.check()
            existing = choose_existing()
            report(f'Watcher owns Pi and closes it on stop. {self.terminal.startup_hint()}')
            self._watch(config, workspace, interval, existing, report, report_error)

    def _watch(self, config: FactoryConfiguration, workspace: Path, interval: float,
               existing: bool, report: Callable[[str], None],
               report_error: Callable[[str], None]) -> None:
        sources = tuple(dict.fromkeys(
            WorkSource(repository.work_source.provider, repository.work_source.reference.casefold())
            for repository in config.repository
        ))
        seen: dict[str, str] = {}
        baselined: set[WorkSource] = set()
        try:
            self.terminal.start(str(workspace), config.foreman_agent_model,
                                config.foreman_agent_effort)
            report('Foreman session ready; model access unverified. '
                   'Native role instructions loaded from the launch directory. '
                   'Forgetful planning access checked; submission is not agent receipt.')
            self._notify_issues(tuple(self.scaffold.unfinished()), seen, report, recovered=True)
            while True:
                for source in sources:
                    issues = self._read_issues(source, config.watcher_label, report_error)
                    if issues is None:
                        continue
                    if not existing and source not in baselined:
                        # Existing durable work must receive replies made while watch was stopped.
                        resumed = tuple(issue for issue in issues if issue.id in seen)
                        self._notify_issues(resumed, seen, report)
                        seen.update((issue.id, issue.revision) for issue in issues)
                        baselined.add(source)
                        report(f'Baseline {source.reference}: {len(issues)} matching issues.')
                        continue
                    self._notify_issues(issues, seen, report)
                self.terminal.wait(interval)
        finally:
            try:
                self.terminal.close()
            except FactoryError as error:
                report_error(str(error))

    def _notify_issues(self, issues: tuple[Issue, ...], seen: dict[str, str],
                       report: Callable[[str], None], *, recovered: bool = False) -> None:
        for issue in issues:
            if seen.get(issue.id) == issue.revision:
                continue
            scaffold = self.scaffold.prepare(issue)
            message = 'Factory issue notification. External issue data: ' + json.dumps({
                'id': issue.id, 'repository': issue.source.reference,
                'number': issue.number, 'title': issue.title, 'url': issue.url,
                'body': issue.body, 'revision': issue.revision, 'recovered': recovered, **scaffold,
            })
            self.terminal.send(message)
            seen[issue.id] = issue.revision
            report(f'Submitted {issue.id} to Pi (submission only).')

    def _read_issues(self, source: WorkSource, labels: tuple[str, ...],
                     report_error: Callable[[str], None]) -> tuple[Issue, ...] | None:
        try:
            return self.tracking.list_issues(source, labels)
        except FactoryError as error:
            report_error(f'{error} Will retry next poll.')
            return None
