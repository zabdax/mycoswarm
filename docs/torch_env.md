# Isolated PyTorch environment

- Location: C:\Users\MIT\.venvs\myco-torch (outside the repo; nothing else touched)
- Interpreter: Python 3.12.10 venv (own site-packages; no system changes, no PATH edits)
- Contents: torch 2.14.1+cpu (CPU-only, cuda=False), numpy 2.5.2 (+ deps)
- Use: C:\Users\MIT\.venvs\myco-torch\Scripts\python.exe <script>
- Purpose: real DQN port of the tabular Q-learner (C09 protocol template)
- Verified: MLP forward pass OK in venv; main python has no torch (isolation confirmed)
