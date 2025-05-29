# Not used
from typing import Any, Dict, List, Optional

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class SearchService:
    def __init__(self):
        settings = get_settings()
        self.endpoint = (
            f"https://{settings.azure_search_service_name}.search.windows.net"
        )
        self.api_key = settings.azure_search_api_key
        self.index_name = settings.azure_search_index_name
        self.credential = AzureKeyCredential(self.api_key)
        self.client = SearchClient(
            endpoint=self.endpoint,
            index_name=self.index_name,
            credential=self.credential,
        )
        logger.info(
            "SearchService initialized",
            endpoint=self.endpoint,
            index_name=self.index_name,
        )

    async def search(
        self,
        query: str,
        filters: Optional[str] = None,
        top: int = 10,
        skip: int = 0,
        query_type: QueryType = QueryType.SEMANTIC,
        semantic_configuration_name: str = "default",
    ) -> List[Dict[str, Any]]:
        """
        Perform a semantic search on the furniture index.

        Args:
            query: The search query
            filters: OData filter expression
            top: Number of results to return
            skip: Number of results to skip
            query_type: Type of search to perform
            semantic_configuration_name: Name of the semantic configuration to use

        Returns:
            List of search results
        """
        try:
            logger.info(
                "Performing search",
                query=query,
                filters=filters,
                top=top,
                skip=skip,
                query_type=query_type,
                semantic_configuration_name=semantic_configuration_name,
            )

            # results = self.client.search(
            #     search_text=query,
            #     filter=filters,
            #     top=top,
            #     skip=skip,
            #     query_type=query_type,
            #     semantic_configuration_name=semantic_configuration_name,
            #     query_caption="extractive",
            #     query_answer="extractive",
            # )

            results = self.client.search(search_text=query)

            # Convert results to list of dicts
            result_list = [dict(result) for result in results]
            logger.info("Search completed", result_count=len(result_list))
            return result_list
        except Exception as e:
            logger.error(
                "Error performing search",
                error=str(e),
                error_type=type(e).__name__,
                exc_info=True,
            )
            return []

    # async def create_index(self, index_definition: Dict[str, Any]) -> bool:
    #     """
    #     Create or update the search index.

    #     Args:
    #         index_definition: The index definition dictionary

    #     Returns:
    #         bool: True if successful, False otherwise
    #     """
    #     try:
    #         logger.info("Creating/updating search index", index_name=self.index_name)
    #         index_client = SearchIndexClient(
    #             endpoint=self.endpoint, credential=self.credential
    #         )

    #         index = SearchIndex(
    #             name=self.index_name,
    #             fields=index_definition["fields"],
    #             semantic_settings=index_definition.get("semantic_settings"),
    #             scoring_profiles=index_definition.get("scoring_profiles", []),
    #             suggesters=index_definition.get("suggesters", []),
    #         )

    #         index_client.create_or_update_index(index)
    #         logger.info("Index created/updated successfully")
    #         return True
    #     except Exception as e:
    #         logger.error(
    #             "Error creating/updating index",
    #             error=str(e),
    #             error_type=type(e).__name__,
    #             exc_info=True,
    #         )
    #         return False

    # async def upload_documents(self, documents: List[Dict[str, Any]]) -> bool:
    #     """
    #     Upload documents to the search index.

    #     Args:
    #         documents: List of documents to upload

    #     Returns:
    #         bool: True if successful, False otherwise
    #     """
    #     try:
    #         logger.info("Uploading documents", document_count=len(documents))
    #         self.client.upload_documents(documents)
    #         logger.info("Documents uploaded successfully")
    #         return True
    #     except Exception as e:
    #         logger.error(
    #             "Error uploading documents",
    #             error=str(e),
    #             error_type=type(e).__name__,
    #             exc_info=True,
    #         )
    #         return False
