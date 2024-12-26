from django.db import models

class FeatureFlags(models.Model):
    llm_article_generation = models.BooleanField(default=False)
    llm_tags_generation = models.BooleanField(default=False)

    def __str__(self):
        return f"LLM Article Generation: {self.llm_article_generation}, LLM Tags Generation: {self.llm_tags_generation}"
