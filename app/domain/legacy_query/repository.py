from app.domain.common.repository_base import RepositoryBase
from app.domain.patner_example.model import PatnerExample


class Repository(RepositoryBase):
    async def find_patner_by_document(self, document: str) -> PatnerExample:
        """Find patner by document
        :param document: The document of the patner

        :return: PatnerExample
        """
        return self.session_db.query(PatnerExample).filter_by(document=document).first()
