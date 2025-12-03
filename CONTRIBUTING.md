# Contributing to Public Issue Tracker

Thank you for considering contributing to the Public Issue Tracker! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs
1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features
1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write/update tests
5. Update documentation
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## 📝 Code Style

### Python
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

### Django
- Follow Django best practices
- Use class-based views where appropriate
- Keep models clean and focused
- Use Django's built-in features

### Templates
- Use semantic HTML
- Follow Tailwind CSS conventions
- Keep templates DRY (Don't Repeat Yourself)
- Add comments for complex logic

### JavaScript
- Use modern ES6+ syntax
- Add comments for complex logic
- Keep functions small and focused

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

```bash
python manage.py test
```

## 📚 Documentation

- Update README.md for major changes
- Add docstrings to new functions/classes
- Update SETUP_GUIDE.md if setup changes
- Add comments for complex code

## 🔄 Development Workflow

1. **Setup Development Environment**
   ```bash
   git clone https://github.com/rr0h/public-issue-tracker.git
   cd public-issue-tracker
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python manage.py migrate
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write code
   - Add tests
   - Update docs

4. **Test Changes**
   ```bash
   python manage.py test
   python manage.py runserver  # Manual testing
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Commit Message Guidelines

Use clear, descriptive commit messages:

- `Add: New feature or functionality`
- `Fix: Bug fix`
- `Update: Changes to existing feature`
- `Refactor: Code restructuring`
- `Docs: Documentation changes`
- `Test: Adding or updating tests`
- `Style: Formatting, missing semicolons, etc.`

Example:
```
Add: Duplicate issue detection with AI

- Implement TF-IDF based similarity detection
- Add location proximity checking
- Update issue creation view to show warnings
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Mobile app development
- [ ] Real-time notifications
- [ ] Advanced analytics
- [ ] Performance optimization
- [ ] Accessibility improvements

### Medium Priority
- [ ] Multi-language support
- [ ] Email notifications
- [ ] SMS integration
- [ ] Advanced search
- [ ] Export functionality

### Good First Issues
- [ ] UI/UX improvements
- [ ] Documentation updates
- [ ] Test coverage
- [ ] Bug fixes
- [ ] Code refactoring

## 🐛 Bug Fix Process

1. Identify the bug
2. Write a test that reproduces it
3. Fix the bug
4. Ensure test passes
5. Submit PR with test and fix

## ✨ Feature Development Process

1. Discuss feature in an issue first
2. Get approval from maintainers
3. Design the feature
4. Implement with tests
5. Update documentation
6. Submit PR

## 📞 Getting Help

- **GitHub Issues**: For bugs and features
- **Email**: rajrohit9377@gmail.com
- **Discussions**: Use GitHub Discussions for questions

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commit history

## 📜 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing others' private information

## 🔒 Security

If you discover a security vulnerability:
1. **DO NOT** open a public issue
2. Email rajrohit9377@gmail.com with details
3. Wait for response before disclosing

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!

---

**Questions?** Feel free to ask in GitHub Issues or Discussions.
