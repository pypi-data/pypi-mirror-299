# HintlyDataAnalisys Documentation

This library is designed to process and analyze text data, perform mathematical computations, and integrate plugins for custom operations. The library supports text normalization, counting specific characters or words, and providing basic mathematical operations like mean, difference, normalization, and more. Additionally, the MatchMaker class allows for text manipulation based on pre-configured rules stored in JSON files.

## Table of contents
 - [Variables](#1-global-variables)
 - [Classes](#2-classes)
   - [Math](#21-math)
   - [Text](#22-text)
   - [MatchMaker](#23-matchmaker)
      - [Plugins](#24-plugins-nested-in-matchmaker)
      - [timeLib](#25-timelib-nested-in-matchmaker)
 - [API](#api-documentation)
   - [Math](#math-operations)
   - [Text](#text-operations)
   - [MatchMaker](#matchmaker)
     - [Plugins](#plugins)
 - [Authors](#authors)
 - [License](#license)
 - [Future Plans](#future-plans)

## 1. **Global Variables**
- **`intrepunctions`**: A list of punctuation marks used for text analysis (e.g., ".", ",", ":", "?", etc.).
- **`whiteSigns`**: A list of whitespace characters (e.g., " ", "\n", etc.).
- **`data`**: JSON data loaded from the file `matchmaker.json` that stores configuration settings.

## 2. **Classes**

#### **2.1. Math**
This class contains mathematical operations for analyzing numerical data.

- **`Mean(analisysData: list)`**: Returns the average of a list of numbers.
- **`Difference(a, b)`**: Calculates the percentage difference between two values `a` and `b`.
- **`Normalize(analisysData: list, normalizeNumber: int)`**: Normalizes the values in `analisysData` to a scale defined by `normalizeNumber`.
- **`MakeInt(value: float, divideNumber: int)`**: Converts a float to an integer by rounding after subtracting `divideNumber`.
- **`AbsoluteDifference(a, b)`**: Returns the absolute difference between two values.
- **`AbsoluteIntPercentDifference(a, b)`**: Returns the absolute percentage difference, converted to an integer.
- **`WeightedAverage(analisysData: list, weights: list)`**: Computes the weighted average of the given data.
- **`NumberRepeat(numbers: list)`**: Returns a dictionary with the count of occurrences of each number in `numbers`.
- **`PercentNumberChance(numbers: list)`**: Returns a dictionary showing the probability (as a percentage) of each number appearing in `numbers`.

#### **2.2. Text**
This class provides utilities for text analysis and manipulation.

- **`CountInterpunctions(text: str)`**: Returns a dictionary with the count of each punctuation mark from `intrepunctions` in the provided `text`.
- **`CountSigns(text: str, lowerSigns: bool)`**: Returns a dictionary of character counts in `text`, either case-sensitive or case-insensitive based on the `lowerSigns` flag.
- **`CountWord(text: str, word: str)`**: Returns the number of times a word appears in the provided `text`.
- **`FilterWordsWithSign(text: str, sign: str, filterType: FilterType)`**: Based on `filterType`, either counts or removes the occurrences of a word (`sign`) from `text`.
- **`NormalizeText(text: str, normalizeType: NormalizeType)`**: Performs various normalization actions (such as deleting punctuation or changing text to lowercase) based on the specified `normalizeType`.
- **`GetWordsFromText(text: str)`**: Splits the provided text into a list of words.

#### **2.3. MatchMaker**
This class is responsible for more advanced text manipulation, including hidden text processing and splitting based on specific rules.

- **`MMSplitText(text: str)`**: Splits the text based on a key defined in the `matchmaker.json` file and returns a list of text segments.
- **`MMHiddenText(text: str)`**: Removes hidden parts of the text enclosed by specific start and end markers from `matchmaker.json`.
- **`MMPasswordText(text: str)`**: Replaces the content between specific markers (start and end) with asterisks for obfuscation.

#### **2.4. Plugins (Nested in MatchMaker)**
This class manages external plugins that can extend the library's functionality.

- **`InstallPlugin(name: str)`**: Installs a plugin by importing it and updating the `matchmaker.json` file.

#### **2.5. timeLib (Nested in MatchMaker)**
This class allows for time-based text operations if the `timeLib` plugin is installed.

- **`Detect(text: str)`**: Detects and replaces time tags in the text if the `timeLib` plugin is available.

## API Documentation

#### **Math Operations**
1. **`Mean(analisysData: list) -> float`**: Calculate the mean of a list of numbers.
   ```python
   Math.Mean([1, 2, 3, 4, 5])  # Returns: 3.0
   ```

2. **`Difference(a: float, b: float) -> float`**: Calculate the percentage difference between `a` and `b`.
   ```python
   Math.Difference(50, 100)  # Returns: 100.0
   ```

3. **`Normalize(analisysData: list, normalizeNumber: int) -> list`**: Normalize a list of numbers to a specified range.
   ```python
   Math.Normalize([1, 2, 3], 10)  # Returns: [3.33, 6.67, 10]
   ```

4. **`AbsoluteDifference(a: float, b: float) -> float`**: Return the absolute difference between two values.
   ```python
   Math.AbsoluteDifference(5, 10)  # Returns: 5
   ```

5. **`WeightedAverage(analisysData: list, weights: list) -> float`**: Calculate the weighted average of a list.
   ```python
   Math.WeightedAverage([3, 4, 5], [1, 2, 1])  # Returns: 4.0
   ```

6. **`NumberRepeat(numbers: list) -> dict`**: Return a dictionary with the number of times each number appears in the list.
   ```python
   Math.NumberRepeat([1, 2, 2, 3])  # Returns: {1: 1, 2: 2, 3: 1}
   ```

#### **Text Operations**
1. **`CountInterpunctions(text: str) -> dict`**: Count how many times each punctuation appears in the text.
   ```python
   Text.CountInterpunctions("Hello, world!")  # Returns: {",": 1, "!": 1}
   ```

2. **`CountSigns(text: str, lowerSigns: bool) -> dict`**: Count each character's appearance in the text, either case-sensitive or case-insensitive.
   ```python
   Text.CountSigns("Hello", True)  # Returns: {"h": 1, "e": 1, "l": 2, "o": 1}
   ```

3. **`CountWord(text: str, word: str) -> int`**: Count how many times a word appears in the text.
   ```python
   Text.CountWord("This is a test. This test is simple.", "test")  # Returns: 2
   ```

4. **`NormalizeText(text: str, normalizeType: NormalizeType) -> str`**: Normalize text by performing actions such as removing punctuation or converting text to lowercase.
   ```python
   Text.NormalizeText("Hello, World!", NormalizeType.LowText)  # Returns: "hello, world!"
   ```

#### **MatchMaker**
1. **`MMSplitText(text: str) -> list`**: Split text based on a key defined in the `matchmaker.json` file.
   ```python
   MatchMaker.MMSplitText("Hello world!")  # Returns: list of segments based on key
   ```

2. **`MMHiddenText(text: str) -> str`**: Remove hidden text segments enclosed by specified markers.
   ```python
   MatchMaker.MMHiddenText("This is {hd}secret{/hd} text.")  # Returns: "This is text."
   ```

3. **`MMPasswordText(text: str) -> str`**: Obfuscate text between markers with asterisks.
   ```python
   MatchMaker.MMPasswordText("Password is {password}12345|{/password} hidden.")  # Returns: "Password is ***** hidden."
   ```

#### **Plugins**
1. **`InstallPlugin(name: str)`**: Install and integrate an external plugin into the library.

   ```python
   MatchMaker.Plugins.InstallPlugin("example_plugin")
   ```
## Authors
#### Franciszek Chmielewski (ferko2610@gmail.com)
##  License
All in LICENSE file.

    MIT Licence

    Copyright (c) 2024 Franciszek Chmielewski.

    Permission is hereby granted to anyone who obtains a copy of this software and associated documentation files (the ‘Software’) to use the Software for personal purposes only, subject to the following conditions:

    1. The Software may not be copied, reproduced, modified or distributed in any form without the prior written consent of the author.
    2. It is not permitted to publish, sublicense, sell, share or transfer the Software to others without the written consent of the author.
    3. It is prohibited to decompile, reverse engineer, modify or create derivative works based on the Software.

    <b>THE SOFTWARE IS PROVIDED ‘AS IS’ WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, WITHOUT LIMITATION, THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIMS, DAMAGES OR OTHER LIABILITIES, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING OUT OF OR RELATING TO THE SOFTWARE OR THE USE OR OTHER ACTIVITIES IN THE SOFTWARE.</b>
## Future Plans
#### Roadmap: [Roadmap](https://trello.com/b/dJ2B3uSM/hintlydataanalisys)
 - Adding more mathematical tools
 - Adding more text tools
 - Adding more plug-ins to MatchMaker.
 - Adding functions to MatchMaker.