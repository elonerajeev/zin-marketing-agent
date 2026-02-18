# Contributing to Zin Marketing Agent

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs
- Use GitHub Issues
- Include steps to reproduce
- Provide error messages and logs
- Mention your environment (OS, Python version)

### Suggesting Features
- Open a GitHub Discussion
- Describe the use case
- Explain why it would be valuable

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add: feature description"
   ```
6. **Push and create Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/zin-marketing-agent.git
cd zin-marketing-agent

# Install dependencies
pip install openai anthropic requests

# Copy environment template
cp config/.env.example .env
# Add your API keys

# Test
./zin "list automations"
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Adding Automations

1. Create n8n workflow
2. Add to `config/automations.json`
3. Test with `./zin "your command"`
4. Document in README

## Testing

- Test single automations
- Test multi-step workflows
- Test error handling
- Test with different LLM providers

## Pull Request Guidelines

- One feature per PR
- Update documentation
- Add examples if applicable
- Ensure all tests pass

## Questions?

Open a GitHub Discussion or reach out via Issues.

Thank you for contributing! 🚀
