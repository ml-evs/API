from typing import List, Optional
from pymatgen.core.periodic_table import Element
from mp_api.core.client import BaseRester, MPRestError
from emmet.core.xas import Edge, Type, XASDoc


class XASRester(BaseRester):

    suffix = "xas"
    document_model = XASDoc  # type: ignore
    primary_key = "xas_id"

    def get_available_elements(
        # TODO implement actual check
        self,
        edge: Optional[Edge] = None,
        spectrum_type: Optional[Type] = None,
        absorbing_element: Optional[Element] = None,
        required_elements: Optional[List[Element]] = None,
    ):
        return [str(e) for e in Element]

    def get_xas_doc(self, xas_id: str):
        # TODO do some checking here for sub-components
        query_params = {"all_fields": True}

        result = self._query_resource(query_params, suburl=xas_id)
        if len(result.get("data", [])) > 0:
            return result["data"][0]
        else:
            raise MPRestError("No document found")

    def search_xas_docs(
        self,
        edge: Optional[Edge] = None,
        absorbing_element: Optional[Element] = None,
        required_elements: Optional[List[Element]] = None,
        formula: Optional[str] = None,
        task_ids: Optional[List[str]] = None,
        num_chunks: Optional[int] = None,
        chunk_size: int = 1000,
        all_fields: bool = True,
        fields: Optional[List[str]] = None,
    ):
        query_params = {
            "edge": str(edge.value) if edge else None,
            "absorbing_element": str(absorbing_element) if absorbing_element else None,
            "formula": formula,
        }  # type: dict

        if task_ids is not None:
            query_params["task_ids"] = ",".join(task_ids)

        if required_elements:
            query_params["elements"] = ",".join([str(el) for el in required_elements])

        return super().search(
            version=self.version,
            num_chunks=num_chunks,
            chunk_size=chunk_size,
            all_fields=all_fields,
            fields=fields,
            **query_params,
        )

    def count_xas_docs(
        # TODO: switch to using core count method
        self,
        edge: Optional[Edge] = None,
        absorbing_element: Optional[Element] = None,
        required_elements: Optional[List[Element]] = None,
        formula: Optional[str] = None,
    ):
        query_params = {
            "edge": str(edge.value) if edge else None,
            "absorbing_element": str(absorbing_element) if absorbing_element else None,
            "formula": formula,
        }

        if required_elements:
            query_params["elements"] = ",".join([str(el) for el in required_elements])

        query_params["limit"] = "1"
        result = self._query_resource(query_params)
        return result.get("meta", {}).get("total", 0)
