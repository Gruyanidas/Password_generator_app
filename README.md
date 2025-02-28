# 📚 Personal Password Generator App

A simple GUI-based application designed to help users generate, save, and manage strong passwords securely. This app runs locally, ensuring your data remains on your machine.

---

## 🚀 Features
- **Password Generator**: Generate strong passwords with customizable options for numeric and special characters.
- **Secure Storage**: Save and retrieve your passwords securely in a local `my_passwords.json` file.
- **Search Functionality**: Quickly search for saved passwords by website name.
- **Clipboard Integration**: Automatically copy generated passwords to your clipboard for convenient use.
- **Interactive UI**: User-friendly interface built using Python's `Tkinter` library.

---

## 🔧 Requirements
To run this project, you need:
- **Python 3.x**
- Required dependencies listed in `requirements.txt`. Install them using:
  ```bash
  pip install -r requirements.txt
  ```

---

## 📝 How to Use
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-generator-app.git
   cd password-generator-app
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python main.py
   ```
4. Follow these steps:
   - **Generate a Password**: Input the number of numeric and special characters required and click "Generate password".
   - **Save Password**: Provide website, email, and password details and hit "Save file".
   - **Search for Password**: Enter website name and hit "Search" to retrieve saved credentials.

---
## 💡 Notes
- This app is designed for **local use only**. Ensure the `my_passwords.json` file is in a secure directory.
- Password data is **not encrypted**; use this app at your own discretion.
- The app is tested on Linux with `xclip` for clipboard support. For Windows users, replace `xclip` usage with `pyperclip` as mentioned in the code.

---

## 🛠️ Built With
- **Python 3.x**
- **Tkinter**: To create the graphical user interface.

---

## 👨‍💻 Author
Developed by **Gruyanidas**.

Feel free to make contributions to this project and improve functionality.

---

## ⚖️ License
This project is open-sourced under the MIT License - feel free to use, modify, and distribute it.