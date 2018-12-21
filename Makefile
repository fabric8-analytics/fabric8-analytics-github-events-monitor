run:
	LOGLEVEL="INFO" GITHUB_TOKEN="${GITHUB_TOKEN}" SLEEP_PERIOD=2 WATCH_REPOS="msehnout/ipc_example" python3 run.py

test:
	pytest ghmonitor/

get-testing-data:
	curl https://api.github.com/events > events.json

docker-run:
	docker run -e LOGLEVEL="INFO" -e GITHUB_TOKEN="$GITHUB_TOKEN" -e SLEEP_PERIOD=10 -e WATCH_REPOS="msehnout/ipc_example" github-monitor

docker-build:
	docker build -t github-monitor .
