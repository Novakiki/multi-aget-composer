# Path configurations
set -gx PATH /usr/local/bin $PATH

# Custom prompt
function fish_prompt
    set_color white
    echo -n (basename (pwd)) " ❯ "
    set_color normal
end

# >>> conda initialize >>>
if test -f /Users/amygrant/miniconda3/bin/conda
    eval /Users/amygrant/miniconda3/bin/conda "shell.fish" "hook" $argv | source
end
# <<< conda initialize <<<

# Ensure conda base is activated in interactive shells
if status is-interactive
    conda activate base
end

# Homebrew (after conda to ensure conda Python takes precedence)
eval (/opt/homebrew/bin/brew shellenv)

# Development tools
fish_add_path /Users/amygrant/.codeium/windsurf/bin 