import sys

from reling.app.app import app
from reling.app.default_content import set_default_content
from reling.app.types import CONTENT_ARG, LANGUAGE_OPT, LANGUAGE_OPT_FROM
from reling.db.models import DialogueExam, Language, TextExam
from reling.utils.scores import format_average_score
from reling.utils.tables import build_table, print_table
from reling.utils.time import format_time, format_time_delta

__all__ = [
    'history',
]

FROM = 'From'
TO = 'To'
TAKEN_AT = 'Taken at'
DURATION = 'Duration'
SCORE = 'Score'

AUDIO_OUTPUT = '🔈'
AUDIO_INPUT = '🎤'


def match(exam: TextExam | DialogueExam, from_: Language | None, to: Language | None) -> bool:
    return ((from_ is None or exam.source_language.id == from_.id)
            and (to is None or exam.target_language.id == to.id))


def get_sort_key(exam: TextExam | DialogueExam) -> tuple:
    return (
        exam.source_language.name,
        exam.target_language.name,
        -exam.started_at.timestamp(),
    )


@app.command()
def history(content: CONTENT_ARG, from_: LANGUAGE_OPT_FROM = None, to: LANGUAGE_OPT = None) -> None:
    """Display exam history, optionally filtered by source or target language."""
    set_default_content(content)
    exams = sorted(
        filter(lambda e: match(e, from_, to), content.exams),
        key=get_sort_key,
    )
    if exams:
        table = build_table(
            headers=[
                FROM,
                TO,
                TAKEN_AT,
                DURATION,
                SCORE,
            ],
            justify={
                FROM: 'left',
                TO: 'left',
                TAKEN_AT: 'left',
                DURATION: 'right',
                SCORE: 'right',
            },
            data=[{
                FROM: ' '.join([
                    exam.source_language.name,
                    *([AUDIO_OUTPUT] if exam.read_source else []),
                ]),
                TO: ' '.join([
                    exam.target_language.name,
                    *([AUDIO_OUTPUT] if exam.read_target else []),
                    *([AUDIO_INPUT] if exam.listened else []),
                ]),
                TAKEN_AT: format_time(exam.started_at),
                DURATION: format_time_delta(exam.finished_at - exam.started_at),
                SCORE: format_average_score([result.score for result in exam.results]),
            } for exam in exams],
            group_by=[
                FROM,
                TO,
            ],
        )
        print_table(table)
    else:
        print('No exams found.', file=sys.stderr)
