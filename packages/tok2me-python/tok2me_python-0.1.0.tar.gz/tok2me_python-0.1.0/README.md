<p align="center">
  <img src="./media/logo.png" width=150 />
</p>

<h1 align="center">tok2me</h1>

<p align="center">
<i>/ʤiː piː tiː miː/</i>
</p>

<!-- Links -->
<p align="center">
  
  <a href="https://www.tok2me.net/">Website</a>
  •
  <a href="https://docs.tok2me.net/">Documentation</a>
</p>

## 🚀 Getting Started

Install with pipx:

```sh
# requires Python 3.10+
pipx install tok2me-python
```

Now, to get started, run:

```sh
tok2me
```

Here are some examples:

```sh
tok2me 'write an impressive and colorful particle effect using three.js to particles.html'
tok2me 'render mandelbrot set to mandelbrot.png'
tok2me 'suggest improvements to my vimrc'
tok2me 'convert to h265 and adjust the volume' video.mp4
git diff | tok2me 'complete the TODOs in this diff'
make test | tok2me 'fix the failing tests'
```


## 🛠 Usage

```sh
$ tok2me --help
Usage: tok2me [OPTIONS] [PROMPTS]...

  tok2me is a chat-CLI for LLMs, empowering them with tools to run shell
  commands, execute code, read and manipulate files, and more.

  If PROMPTS are provided, a new conversation will be started with it. PROMPTS
  can be chained with the '-' separator.

  The interface provides user commands that can be used to interact with the
  system.

  Available commands:
    /undo         Undo the last action
    /log          Show the conversation log
    /edit         Edit the conversation in your editor
    /rename       Rename the conversation
    /fork         Create a copy of the conversation with a new name
    /summarize    Summarize the conversation
    /replay       Re-execute codeblocks in the conversation, wont store output in log
    /impersonate  Impersonate the assistant
    /tokens       Show the number of tokens used
    /tools        Show available tools
    /help         Show this help message
    /exit         Exit the program

Options:
  -n, --name TEXT        Name of conversation. Defaults to generating a random
                         name.
  -m, --model TEXT       Model to use, e.g. openai/gpt-4o,
                         anthropic/claude-3-5-sonnet-20240620. If only
                         provider given, a default is used.
  -w, --workspace TEXT   Path to workspace directory. Pass '@log' to create a
                         workspace in the log directory.
  -r, --resume           Load last conversation
  -y, --no-confirm       Skips all confirmation prompts.
  -n, --non-interactive  Force non-interactive mode. Implies --no-confirm.
  --system TEXT          System prompt. Can be 'full', 'short', or something
                         custom.
  --no-stream            Don't stream responses
  --show-hidden          Show hidden system messages.
  -v, --verbose          Show verbose output.
  --version              Show version and configuration information
  --help                 Show this message and exit.
```
