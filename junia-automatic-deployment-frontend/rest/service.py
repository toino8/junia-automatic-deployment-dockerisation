import httpx
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Chat(BaseModel):
    """Base class for what a generic POST request to an LLM should contain.

    * The model you want to use.
    * The temperature.
    * The messages you send.
    """

    model: str
    temperature: float | None = Field(ge=0.0, le=1.0, default=0.7)
    messages: list[dict[str, str]]


class LLMClient:
    """The client used to communicate with the backend LLM."""

    def __init__(
        self,
        root_url: str,
    ) -> None:
        self.client = httpx.Client(verify=True)
        self.root_url = root_url

    def _generate_request(self, chat: Chat) -> tuple[dict, dict, str]:  # type:ignore
        """Generates the 3 parts necessary for the request via the HTTPX library.

        This function generates the header, body, and url for a POST request via HTTPX.

        Args:
            chat (Chat): A Chat class.

        Returns:
            tuple[dict, dict, str]: The header, body, and url.
        """
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        body = chat.messages

        route = f"http://{self.root_url}/v1/models/{chat.model}/temperature/{chat.temperature}/"

        return headers, body, route  # type: ignore

    def post(
        self,
        chat: Chat,
    ):
        """POST request."""
        headers, body, route = self._generate_request(chat=chat)

        try:
            response = self.client.post(
                url=route,
                headers=headers,
                json=body,
                timeout=180.0,
            )
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            raise
        except httpx.HTTPStatusError as exc:
            print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
            )
            raise

        return response


class BackendConfig(BaseSettings):
    backend_service_name: str = Field(
        alias="BACKEND_SERVICE_NAME",
        default="0.0.0.0:8000",
    )


cfg = BackendConfig()

client = LLMClient(root_url=cfg.backend_service_name)
