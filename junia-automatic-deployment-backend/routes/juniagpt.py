from typing import Annotated

import httpx
from config.schemas import Chat, OllamaConfig, PromptIn, PromptOut
from fastapi import APIRouter, Body, status

router = APIRouter(prefix="/v1")


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

        body = {
            "model": chat.model,
            "messages": chat.messages,
            "stream": False,
            "options": {"temperature": chat.temperature},
        }

        route = f"http://{self.root_url}/api/chat"

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


ollama_cfg = OllamaConfig()
client = LLMClient(root_url=ollama_cfg.ollama_service_name)


@router.post(
    "/models/{model}/temperature/{temperature}/",
    tags=["chat"],
    response_model=PromptOut,
    status_code=status.HTTP_200_OK,
    summary="Converse with JuniaGPT.",
)
def chat(
    prompts: Annotated[
        list[PromptIn],
        Body(
            examples=[
                [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "this is a test"},
                ],
            ],
        ),
    ],
    model: str,
    temperature: float,
):
    messages = [{"role": prompt.role, "content": prompt.content} for prompt in prompts]

    chat = Chat(model=model, temperature=temperature, messages=messages)

    response = client.post(chat=chat)

    message = response.json()["message"]["content"]

    return PromptOut(answer=message)
