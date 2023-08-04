---
layout: post
title:  "Vim Plugin using Vim9 Script"
date:   2023-08-03 10:16:45 +0200
categories:
tags: vim vim9script vim-plugin howto
keywords: vim, vim9script
---

If you are a longtime user of [Vim](https://www.vim.org) there are occasions
where you may want to extend the functionality of Vim by writing your own
plugin. The release of [Vim9 script](https://vimhelp.org/vim9.txt.html) has
made the task less intimidating since the new scripting language [resembles
Python](https://github.com/yegappan/VimScriptForPythonDevelopers).
This blog post is not a beginner guide but rather a collection of thoughts from
my experience developing 
[autosuggest](https://github.com/girishji/autosuggest.vim) and
[vimcomplete](https://github.com/girishji/vimcomplete).

If you are on the fence deciding whether to implement your idea in
[Lua](https://www.lua.org) for
[Neovim](https://neovim.io/) or [Vim9script](https://vimhelp.org/vim9.txt.html)
for [Vim](https://www.vim.org), I have some opinions. Even
though legacy Vim script works on both Vim and Neovim I intentionally did not
learn it because, well, it is just weird and unreadable.

Both Lua and Vim9script are compiled into bytecode (unlike legacy script). I wrote a few
non-trivial plugins in Lua before switching over to Vim9script. I prefer the
latter because the code tends to be more compact, has more advanced language
features for functional programming (closures with lambdas, for instance), has
better regex support, and offers smoother interface to Vim's APIs. But Lua is
its own fun language to program in and Neovim keeps experimenting with new
features. Ultimately it boils down to preference. If Vim9script tickles your
curiosity then read on.

## Directory Structure

The first step in writing a plugin is to organize your folders. Vim expects
certain folder names. Here is a typical organization for github hosted
repositories.

```
plugin_name
├── LICENSE
├── README.md
├── autoload
│   ├── foo.vim
│   └── bar.vim
├── doc
│   └── plugin_name.txt
└── plugin
    └── plugin_name.vim
```

Your main directory name should be the name of the plugin. Under that
directory, the plugin should have a `plugin` and an `autoload` directory:

- The `plugin` directory sets up the plugin. It should include the commands and
  keybindings that you want in your plugin. The file `plugin_name.vim` gets
  sourced first, followed by other files in this directory.
- The `autoload` directory holds the meat of the plugin. It is only loaded when
  one of the commands defined in the `plugin` directory gets called. On-demand
  loading keeps Vim's initialization faster.
- `doc` directory is optional but highly recommended. Learn the Vim help file
  syntax. You could include even more information here than in `README.md`.
- In addition, you may need an `import` directory if you wish to export
  functions for use in other plugins.

**Note: Vim has extensive documentation. Anytime you have doubt over `foo` try
`:helpgrep foo` or `:h foo<tab>` (with `wildmenu`) or use
[autosuggest](https://github.com/girishji/autosuggest.vim).**

Since `plugin/plugin_name.vim` gets sourced first, include the following
boilerplate code at the top.

```
if !has('vim9script') ||  v:version < 900
    " Needs Vim version 9.0 and above
    finish
endif
vim9script
g:loaded_plugin_name = true
```

All other files should include `vim9script` at the top. In order to use
functions defined in another script you have to use the `import` directive.
From a script in `plugin` directory you could define a command as follows.

```
import autoload '../autoload/foo.vim'
command! -nargs=0 MyCommand foo.SomeFunction()
```

In the above example, `SomeFunction()` needs to be exported (`:h vim9-export`)
from `foo.vim`.

Also, make use of `User` (`:h User`) auto-command event to synchronize parts of initialization.

## Language Features

[Vim9script](https://vimhelp.org/vim9.txt.html) is fairly easy to learn. You
can also pick up some [advanced
insights here](https://github.com/lacygoill/wiki/blob/main/vim/vim9.md). If you
are familiar with Python there is [VimScript For Python
Developers](https://github.com/yegappan/VimScriptForPythonDevelopers). Finally,
here are some suggestions to make your programming task more fun.

### Lambda Expressions

If you are using any type of data manipulation lambda expressions (`:h lambda`)
come in handy. You can use them with usual suspects `filter()`, `map()`, `reduce()`, `sort()` etc.

Functions can be chained using `->` operator. Use the `arg->func()` idiom consistently
throughout. Keep your code readable and bloat-free.

### Meta Tables

Vim9script will have _class_ (`:h class`) in the near future. In the meantime, you can emulate
an object (encapsulation) using a simple dictionary and function references
(`:h funcref()`, `:h function()`).

```
def NewMyObject(someArg: bool): dict<any>
    var contents = {
        property1: [],
        property2: someArg,
    }
    contents->extend({
        functionName1: function(FunctionName1, [contents]),
    })
    return contents
enddef

def functionName1(obj: dict<any>, optionalArg: number)
    var foo = obj.property1
enddef

var myObj = NewMyObject(true)
var fnArg = 22
myObj.functionName1(fnArg)
```

### Options

Users of your plugin may need to set options. Use a dictionary to encapsulate
all options. It is best not to use a global variable for each option, since they
pollute global namespace. You can use a global function that takes a dictionary argument to
set the options. There is also a possibility to use exported function, but this
limits the users to only use Vim9script for configuration. So the former method
is preferred.

In your `autoload/options.vim` you can define the options.

```
export var myOptions: dict<any> = {
    option1: '',
    option2: false,
    option3: [],
}
```

In `plugin/plugin_name.vim` define a global function to set options.

```
import autoload '../autoload/options.vim'

def! g:PluginNameOptionsSet(opts: dict<any>)
    options.myOptions->extend(opts)
enddef
```

### Strings

Be familiar with `==#`, `==?`, `=~#`, `=~?`, `!~`, `match()`, `matchstr()`,
`matchlist()`, `\c`, `\v`, `"` vs `'` etc. See help files.

Use `$'sometext {var}'` as opposed to `"sometext " .. var`.

### Debug

For the most part `echom` in scripts is adequate. You can view the messages
using `:messages`. For checking regex you can use `:echo
'teststring' =~ 'pattern'` or `:echo matchstr('foo', 'pattern')`.

### Disassemble

Sometimes you may ask yourself if it is worth caching a dictionary key
value outside a loop, and discover that Vim9 compiler does not do loop optimization.
You can verify using `:disassembly` that it uses LOADSCRIPT and
USEDICT instructions inside the loop when value is not
cached.

```
% vim -Nu NONE -S <(cat <<'EOF'                                                                                       1 :(   
    vim9script
    var foo = {x: 1, y: 2}
    def Func()
        var fooy = foo.y
        for i in range(5)
            # echom fooy     # good: using cached value
            echom foo.y      # not good
        endfor
    enddef
    disa Func
EOF
)
```

### Asynchronous Execution

Vim offers `job_start()` for truly parallel execution (on a multicore system). You can spawn a new
process and wait for output. However, there is also a lightweight option that offers
concurrent execution. It may sound non-intuitive but you can use
`timer_start()` with `0` timeout to schedule your function for execution at a
later time when Vim's main-loop is free. You can also pass arguments to
callback, for example, `timer_start(0, function(MyWorker, [arg1, arg2]))`.
Typically you break down your long running task into batches (say you want to
search a few thousand lines then search in batches of a thousand lines each).
Each batch can be scheduled using `timer_start()` as above, with one of the arguments to
`MyWorker()` being the index into a batch data array. These tasks should be chained by
having `MyWorker()` call the next `timer_start()` (for the next batch). The
magic here is that Vim schedules any newly typed keystrokes between each
`MyWorker()` invocation. Even though Vim is single-threaded your plugin remains
responsive to keystrokes even while working on a long running task.

### Performance Measurement and Timing

Calling `reltime()` before and after a code section measures execution time.

```
var start = reltime()

# ... do something ...

echom $'Elapsed time: {start->reltime()->reltimestr()}'
```

You can abort a task if it goes over a timeout. Use `reltimefloat()` for
that.

```
var start = reltime()
const timeout = 2000 # millisec

while true

    # ... process a batch ...

    if (start->reltime()->reltimefloat() * 1000) > timeout
        break
    endif
endwhile
```
