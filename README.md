# Integrated Smart Scene Automation & Hands-Free Accessibility System

A responsive, lightweight, context-aware web application paired with hands-free control mechanisms to bridge the gap between everyday intent, physical accessibility, and smart household automation.

---

## 🛠️ Project Overview

Modern residential environments often rely on manual control for everyday appliances and software lists. Isolated smart home tools lack coordination, forcing users—especially those with mobility or dexterity limitations—to manually manipulate multiple interfaces, apps, or switches. 

This project delivers a **unified, responsive web dashboard and voice-enabled control system** that simplifies task/grocery management, automates household routines, and provides hands-free accessibility through natural language parsing and intelligent categorization.

---

## ✨ Key Features

### 💻 1. Core Architecture & Universal UI
* **Responsive & Zero-Install Web App:** Built using lightweight **HTML5, CSS3, and Vanilla JavaScript**. Opens instantly via any web browser on mobile or desktop without requiring app store installation or complex dependencies.
* **Dual-Category Focus:** Clean, uncluttered views dedicated exclusively to **Tasks** and **Groceries** to keep daily organization simple and actionable.
* **Client-Side Data Persistence:** Integrates directly with browser `LocalStorage`, ensuring data is stored locally and never lost on page refresh or browser restarts.

### 🎙️ 2. Intelligent Voice & Smart Keyword Input
* **Native Voice-to-Text Processing:** Powered by the browser-native `Web Speech API`, enabling effortless hands-free command entry via a single microphone toggle.
* **Contextual Voice Guidance:** Includes clear visual visual cues and helper prompts inside the speech input modal (e.g., *"Say 'groceries' or food item names to automatically route items"*).
* **Smart Keyword & Intent Routing:** Automatically parses spoken or typed input for trigger keywords or food-related terms to route items instantly to either the **Groceries** or **Tasks** section.
* **Manual Control Fallback:** Full fallback support with standard text input boxes, manual category dropdown selectors, and native date/time pickers for quiet or high-noise environments.

### 📅 3. Dynamic Organization & Time Views
* **Hierarchical Time Sorting:** Automatically organizes active tasks and grocery items into structured chronological views:
  * **Today:** Items due or tagged for the current day.
  * **Upcoming:** Items scheduled for future dates.

---

## 🏗️ System Architecture

```
                                  +------------------------------+
                                  |     User Input (Voice/Text)   |
                                  +--------------+---------------+
                                                 |
                                                 v
                                  +------------------------------+
                                  |     Web Speech API / Inputs  |
                                  +--------------+---------------+
                                                 |
                                                 v
                                  +------------------------------+
                                  | Smart Intent & Keyword Parser|
                                  +--------------+---------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                                                   |
                       v                                                   v
         +---------------------------+                       +---------------------------+
         |     Groceries Section     |                       |       Tasks Section       |
         +-------------+-------------+                       +-------------+-------------+
                       |                                                   |
                       +-------------------------+-------------------------+
                                                 |
                                                 v
                                  +------------------------------+
                                  |  Hierarchical Time Engine    |
                                  |      (Today / Upcoming)      |
                                  +--------------+---------------+
                                                 |
                                                 v
                                  +------------------------------+
                                  |   Browser LocalStorage Sync  |
                                  +------------------------------+
```

---

## 📑 Functional Requirements

| Category | Requirement | Implementation |
| :--- | :--- | :--- |
| **User Interface** | Responsive, lightweight, clean UX | Pure HTML5, CSS3 (Flexbox/Grid), Vanilla JS |
| **Voice Input** | Hands-free voice recognition | Browser `Web Speech API` (`webkitSpeechRecognition`) |
| **Categorization** | Automatic keyword sorting | Regex & String Keyword Engine |
| **Fallback Controls**| Manual entry option | Native HTML forms, dropdowns, and date-time pickers |
| **Data Storage** | Local offline storage | Browser `window.localStorage` API |
| **Time Grouping** | Chronological ordering | Date comparison logic (`Today` vs `Upcoming`) |

---

## 🚀 Quick Start & Installation

### Prerequisites
* Any modern browser supporting the Web Speech API (e.g., Google Chrome, Microsoft Edge, Safari, Brave).

### Running Locally
1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/smart-scene-accessibility.git
   cd smart-scene-accessibility
   ```
2. Open `index.html` directly in your browser:
   * **Windows:** Double-click `index.html` or run `start index.html` in PowerShell.
   * **macOS:** Run `open index.html` in Terminal.
   * **Linux:** Run `xdg-open index.html`.

---

## 💡 Usage Guide

1. **Voice Entry:**
   * Click the **Microphone** icon.
   * Speak clearly into your mic (e.g., *"Buy milk and eggs for groceries tomorrow"*).
   * The app automatically detects "groceries", extracts the item name, and places it in the **Groceries** tab under **Upcoming**.
2. **Manual Entry:**
   * Type your item into the input field.
   * Optionally choose the Category (**Tasks** or **Groceries**) and set a Due Date.
   * Click **Add Item**.
3. **Filtering & View:**
   * Toggle between **Today** and **Upcoming** to view your scheduled tasks and items.
4. **Item Actions:**
   * Click the checkbox next to any item to mark it as completed.
   * Click the delete icon to remove an item permanently.

---

## 🔮 Future Enhancements & Hardware Roadmap

* **ESP32 / Microcontroller Integration:** Send direct HTTP/WebSocket commands from the dashboard to physical ESP32 relay modules to control physical lights, fans, and smart locks.
* **Offline Voice Parsing:** Implement lightweight, client-side offline speech processing model (e.g., Vosk / PocketSphinx) for environments without internet connectivity.
* **Home Assistant MQTT Sync:** Connect list updates and voice triggers to Home Assistant via MQTT for broader IoT ecosystem automation.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
