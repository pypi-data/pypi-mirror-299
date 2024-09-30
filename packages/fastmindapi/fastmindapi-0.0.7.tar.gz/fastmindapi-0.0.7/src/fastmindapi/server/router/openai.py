from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Request

PREFIX = "/openai"

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    max_completion_tokens: int = None
    logprobs: bool = False
    top_logprobs: int = 10
    stop: list[str] = None

    model_config=ConfigDict(protected_namespaces=())


def chat_completions(request: Request, item: ChatRequest):
    server = request.app.state.server
    try:
        assert item.model in server.module["model"].loaded_models
    except AssertionError:
        return f"【Error】: {item.model} is not loaded."
    
    outputs = server.module["model"].loaded_models[item.model].chat(
        messages=item.messages, 
        max_completion_tokens=item.max_completion_tokens,
        logprobs=item.logprobs,
        top_logprobs=item.top_logprobs,
        stop=item.stop
    )
    return outputs

def get_openai_router():
    router = APIRouter(prefix=PREFIX)

    router.add_api_route("/chat/completions", chat_completions, methods=["POST"])
    return router