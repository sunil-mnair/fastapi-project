import os

from dotenv import load_dotenv


load_dotenv()


def _required_setting(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"Missing required environment variable: {name}")
	return value


OPENAI_API_KEY = _required_setting("OPENAI_API_KEY")
SECRET_KEY = _required_setting("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")