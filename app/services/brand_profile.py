from dataclasses import dataclass, field


@dataclass
class BrandProfile:
    """Configuration that defines the brand's content identity."""

    name: str
    description: str
    target_audience: str
    content_goals: list[str] = field(default_factory=list)
    style_guidelines: list[str] = field(default_factory=list)