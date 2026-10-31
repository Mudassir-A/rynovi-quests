"""Day 2 · The job board bouncer

Job postings arrive from scrapers and forms, and they're messy. Your job: let the good ones in
as clean Pydantic models, and turn the bad ones away with a clear reason.

Run `python quest.py 2` after each TODO.
"""

from pydantic import (
    BaseModel,
    HttpUrl,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)  # noqa: F401


class JobPosting(BaseModel):
    title: str
    company: str
    url: HttpUrl
    salary_lpa: float | None = Field(default=None, ge=0)
    remote: bool = False
    location: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = " ".join(value.split())

        if not value:
            raise ValueError("title can't be empty")

        return value

    @model_validator(mode="after")
    def validate_location(self):
        if not self.remote and not self.location:
            raise ValueError("location is required for on-site jobs")

        return self


def parse_postings(raw: list[dict]) -> tuple[list[JobPosting], list[str]]:
    valid_postings = []
    errors = []

    for index, record in enumerate(raw):
        try:
            posting = JobPosting.model_validate(record)
            valid_postings.append(posting)
        except ValidationError as e:
            error = e.errors()[0]

            field = str(error["loc"][0]) if error["loc"] else "posting"
            message = error["msg"]

            errors.append(f"record {index}: {field}: {message}")
    return valid_postings, errors
