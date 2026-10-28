# Contributing

Keep the scope focused on accurate, inspectable architecture packages. Reproduce a failure before changing behavior, add a regression test when appropriate, and explain how the fix affects installation or verification.

Run from the repository root with Python 3.12+:

```sh
python -m unittest discover -s visualize-project-skill/tests -v
python visualize-project-skill/tests/evaluate_validator.py
python -m compileall -q visualize-project-skill
```

The test suite uses temporary directories, subprocesses, and fault injection. It does not install a user-global skill or call external services. Tests need permission to create and delete temporary directories.

Instruction changes must keep the portable skill and the three target wrappers aligned. Preserve Cursor-specific frontmatter. Check referenced paths and both mode contracts. Do not treat a structural test as an agent evaluation: behavioral changes need recorded host/model versions, repository input, prompt, produced artifacts, renderer version, and a human evidence/visual review using the verification rubric.

Do not include credentials, private source, or private architecture artifacts in issues or contributions. Until a public remote and private security-reporting channel exist, avoid posting vulnerability details publicly; request a private contact from the maintainer.

No deployment or release build is needed: the distribution is the portable directory plus wrappers and installer. Before release, install from a fresh copy, run all checks, review the MIT license, and complete real host workflow evaluations. CI results and release history must be linked only after they exist.
