from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
import json
import re

# Import the restaurant agent dispatcher
from agents.core.langgraph.agent_dispatcher import agent_dispatch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="web/templates")
JSON_FENCE_REGEX = re.compile(r'```json\s*(\{.*?\})\s*```', re.S)

class AgentRequest(BaseModel):
    agent_name: str
    message: str
    identifier: str | None = None

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/agent")
async def call_agent(req: AgentRequest):
    try:
        logger.info(f"[agent_dispatch] Dispatching {req.agent_name} for identifier: {req.identifier}")
        
        context = {
            "identifier": req.identifier,
        }
        
        raw = agent_dispatch(
            agent_name=req.agent_name,
            message=req.message,
            context=context
        )
        
        # Log the raw response
        logger.info(f"Raw agent response: {raw}")
        
        # Extract the JSON content from the response
        content = None
        if hasattr(raw, 'content'):
            logger.info(f"Response has content attribute: {raw.content}")
            if isinstance(raw.content, list):
                # Get the text from the first content item
                text = raw.content[0].get('text', '') if raw.content else ''
                logger.info(f"Extracted text from content: {text}")
                # Try to find JSON in the text
                match = JSON_FENCE_REGEX.search(text)
                if match:
                    logger.info(f"Found JSON in code fence: {match.group(1)}")
                    content = json.loads(match.group(1))
                elif "{" in text and "}" in text:
                    try:
                        json_str = text[text.index("{"):text.rindex("}")+1]
                        logger.info(f"Attempting to parse JSON from text: {json_str}")
                        content = json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse JSON from text: {e}")
                        pass
            else:
                try:
                    logger.info(f"Attempting to parse content directly as JSON: {raw.content}")
                    content = json.loads(raw.content)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse content as JSON: {e}")
                    pass
        
        if content:
            return JSONResponse(content)
        else:
            logger.error("Could not parse any JSON from the response")
            return JSONResponse({"error": "Could not parse agent response"})
            
    except Exception as e:
        logger.error("Agent dispatch failed", exc_info=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
