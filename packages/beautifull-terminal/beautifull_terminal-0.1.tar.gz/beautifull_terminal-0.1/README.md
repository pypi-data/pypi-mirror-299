# BeautifulTerminal

**BeautifulTerminal** is a Python library that automatically beautifies your terminal output by adding colors based on message content. No extra setup is required after importing the library!

## Features

- **Automatic Colors**: 
  - Errors are displayed in red.
  - Warnings are displayed in yellow.
  - Success messages are displayed in green.
  - Normal messages are displayed in white.
  
- **Easy Integration**: 
  - Simply import the library, and it starts working right away.
  
- **Customizable**: 
  - You can easily modify color codes to suit your preferences.

## Installation

To install the library, use `pip`:

```bash
pip install beautifull_terminal
```

## Usage

After installing, you can use it with just a simple import:

```python
import beautifull_terminal

print("This is a normal message.")
print("Error: Something went wrong!")
print("Warning: Proceed with caution!")
print("Success: Operation completed!")
```

### Output Example

- Normal Message: White
- Warning: Yellow
- Error: Red
- Success: Green

## Customization

You can modify the color codes in the library if you want to change the appearance of the outputs. This allows you to adapt it to your preferred terminal theme or personal preference.

## Deactivation

If you need to temporarily disable the color formatting, you can do so:

```python
import beautifull_terminal as bt
bt.disable()  # Temporarily disable color formatting
```

To re-enable:

```python
bt.enable()
```

## License

This project is licensed under the MIT License.

## Contributions

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

## Contact

For any inquiries or feedback, please reach out via the [GitHub repository](https://github.com/StarGames2025/beautifull_terminal).