# Hackathon Delivery Guide

## Problem statement

People with limited mobility, dexterity, vision, or temporary injury often cross several interfaces just to manage a home and daily responsibilities. Existing tools are fragmented, cloud-dependent, and frequently treat accessibility as an add-on.

## Solution

AURA provides one calm, accessible surface for intent. The user speaks, types, or taps; AURA classifies the request, performs a visible action, and preserves a traceable state. The included simulation proves the full software workflow without risky or unreliable hardware dependencies.

## Workflow

1. User supplies voice, text, switch, or form input.
2. Browser speech recognition converts voice to text when supported.
3. FastAPI validates the request.
4. The intent engine routes it to task, grocery, device, or emergency handling.
5. SQLite stores planning data and audit events; the simulation adapter changes device state.
6. The dashboard refreshes and shows immediate confirmation.
7. Later, the simulation adapter can be replaced by an MQTT adapter without changing the UI.

## Recommended team split (5 members)

| Owner | Responsibility | Demo evidence |
|---|---|---|
| 1. Product/UI | UX, accessibility, responsive layout | Mobile/desktop + contrast mode |
| 2. Frontend | API state, voice, commands, interactions | Live command execution |
| 3. Backend | FastAPI, validation, SQLite, tests | Swagger and passing pytest |
| 4. Intelligence | Intent rules, dates, multilingual roadmap | Explainable routing examples |
| 5. Hardware/pitch | ESP32/MQTT adapter, low-voltage circuit, story | LED prototype or simulator |

## Judging narrative

- **Impact:** improves independence and reduces interface burden.
- **Innovation:** planning and ambient automation share one intent engine.
- **Feasibility:** complete offline-capable local software path; no hardware needed for judging.
- **Scalability:** adapter architecture supports devices, rooms, languages, and care networks.
- **Responsibility:** consent-led design, local persistence, visible actions, safe emergency simulation.

## Hardware demo bill of materials

- ESP32 development board
- 2 LEDs, 220 Ω resistors, breadboard, jumper wires
- Optional DHT11/DHT22 sensor
- USB cable and 5 V power

Use an LED on a GPIO as the “light” appliance and a second LED as fan status. Do not connect mains voltage at the event. The next implementation step is an MQTT adapter using Mosquitto and PubSubClient.

## Three-minute pitch flow

**0:00–0:30 — Problem:** demonstrate how fragmented controls create friction.

**0:30–1:30 — Live story:** reset the demo, use voice to turn on a light, add groceries for tomorrow, then complete a care task.

**1:30–2:15 — Accessibility:** keyboard controls, high contrast, typed fallback, hold-to-activate SOS.

**2:15–2:45 — Architecture:** show `/docs`, SQLite, test results, and hardware adapter seam.

**2:45–3:00 — Close:** “AURA does not make a home smarter by adding screens. It makes the environment respond to human intent.”

## Honest limitations

Web Speech support varies by browser and may use an online service. This prototype is not an emergency service or medical device. Device states are simulated until the MQTT adapter is connected.
