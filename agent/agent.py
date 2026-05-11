import asyncio
import logging
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, silero

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voice-agent")


class VoiceAssistant(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a helpful voice assistant in a LiveKit video room. "
                "Keep responses concise and conversational. "
                "When users ask questions, answer clearly and briefly."
            )
        )


async def entrypoint(ctx: JobContext):
    logger.info(f"Agent joining room: {ctx.room.name}")
    await ctx.connect()

    session = AgentSession(
        stt=openai.STT(model="whisper-1"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
        vad=silero.VAD.load(),
    )

    await session.start(
        room=ctx.room,
        agent=VoiceAssistant(),
    )

    await session.generate_reply(
        instructions="Greet the user and let them know you are ready to help."
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
