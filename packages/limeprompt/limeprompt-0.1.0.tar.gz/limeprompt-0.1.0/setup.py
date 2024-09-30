# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limeprompt']

package_data = \
{'': ['*']}

install_requires = \
['anthropic>=0.34.2,<0.35.0', 'pydantic>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'limeprompt',
    'version': '0.1.0',
    'description': 'Light weight prompting and parsing library for LLM models',
    'long_description': '# Limeprompt 🍋\n\nLightweight prompting and parsing library for LLM models.\n\n## What is Limeprompt?\n\nLimeprompt is an opinionated and lightweight prompting and parsing library for LLM models. It aims to make it easy to generate structured outputs from language models. The library is designed to be simple to use, with a single use-case in mind: generating structured outputs from language models. There wont be any support for multi-agent or complex prompting use-cases.\n\n## Installation\n\n```bash\npip install limeprompt\n```\n\n## Example Usage\n\nHere\'s a simple example to get you started:\n\n```python\nfrom anthropic import Anthropic\nfrom pydantic import BaseModel\nfrom limeprompt import Limeprompt\n\n# Define your output structure\nclass Email(BaseModel):\n    subject: str\n    message: str\n\n# Set up your Anthropic client\nanthropic_client = Anthropic(api_key=\'your-api-key\')\n\n# Create a Limeprompt instance\nlp = Limeprompt(\n    model_client=anthropic_client,\n    model_name=\'claude-3-5-sonnet-20240620\',\n    prompt="Write an email to {name} about {topic}",\n    variables={"name": "Alice", "topic": "limes"},\n    output_model=Email,\n    max_tokens=1024\n)\n\n# Run and get your zesty results!\nresult = lp.run()\n\nprint(f"Subject: {result.output.subject}")\nprint(f"Message: {result.output.message}")\n```\n\n## Not\n\n## Contributing\n\nYou are welcome to open issues or submit PRs. Here\'s my todo list for the library:\n\n- [ ] Add support for OpenAI\n- [ ] Modularize the prompting techniques\n- [ ] Add support for few-shot prompting\n\n## License\n\nLimeprompt is released under the MIT License. Feel free to use it in your projects.\n',
    'author': 'Abbas J',
    'author_email': 'abbas@altair.so',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/iam-abbas/limeprompt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
