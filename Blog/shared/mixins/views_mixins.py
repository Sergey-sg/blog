from apps.interaction.models import Score, CommentArticle


class ScoreCommentMixin:
    @staticmethod
    def get_score_for_comment(author, article):
        try:
            score = Score.objects.get(author=author, article=article)
            if score:
                return [True, score]
        except Exception:
            return [False]
        else:
            return [False]


class CommentScoreMixin:
    @staticmethod
    def get_comments_for_score(author, article):
        try:
            comments = CommentArticle.objects.filter(author=author, article=article)
            if comments:
                return [True, comments]
        except Exception:
            return [False]
        else:
            return [False]
