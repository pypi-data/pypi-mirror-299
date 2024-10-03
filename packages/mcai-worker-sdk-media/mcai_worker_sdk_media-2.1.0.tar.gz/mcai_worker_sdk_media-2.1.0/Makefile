include .env
export

all: standard media

standard:
	cargo build --features extension-module
	maturin build --release --find-interpreter --sdist --out ./dist --features extension-module
	TWINE_PASSWORD=${GITLAB_REG_PWD} TWINE_USERNAME=${GITLAB_REG_USR} twine upload --verbose --repository-url https://gitlab.com/api/v4/projects/26202923/packages/pypi dist/*.whl
	TWINE_PASSWORD=${TWINE_PWD} TWINE_USERNAME=__token__ twine upload dist/*.whl
	rm -rf dist/*

media:
	cargo build --features "media, extension-module"
	maturin build --release --find-interpreter --sdist --out ./dist --features "media, extension-module"
	TWINE_PASSWORD=${GITLAB_REG_PWD} TWINE_USERNAME=${GITLAB_REG_USR} twine upload --repository-url https://gitlab.com/api/v4/projects/26202923/packages/pypi dist/*
	TWINE_PASSWORD=${TWINE_PWD} TWINE_USERNAME=__token__ twine upload dist/*
	rm -rf dist/*
