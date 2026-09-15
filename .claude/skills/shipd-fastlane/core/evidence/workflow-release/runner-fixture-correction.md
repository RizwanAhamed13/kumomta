# Runner fixture correction

The first release pass ran 163 plugin fixtures successfully and 28 external runner fixtures with one failure. The XML fixture supplied literal backslash sequences instead of actual control characters and expected an extra escaped backslash. It therefore did not exercise the intended sanitizer path.

The corrected fixture constructs actual ESC, NUL, vertical-tab, lone-surrogate and noncharacter values, requires their safe XML representations, parses the resulting XML and checks that decoded raw events retain the exact original input. The runner implementation is unchanged. The original fixture, first failed receipt and log remain here. This is synthetic harness validation, not candidate execution.
