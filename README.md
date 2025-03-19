# APS Dataset - JSON Format Explanation

## Description
This document explains the structure of the APS dataset after being converted into JSON format. The dataset contains citation cascades, where each cascade represents how a scientific paper is cited over time, including intermediary citations. The JSON format provides a structured representation of this citation flow, making it easier for data analysis and processing.

## JSON Data Format
The converted dataset is stored as a list of JSON objects, where each object represents a single citation cascade.

## JSON Structure
Each JSON object consists of five key fields:

```json
[
    {
        "cascade_id": 1,
        "original_user_id": 1,
        "timestamp": -2414170800,
        "number_of_participants": 6,
        "participants": [
            { "path": "1", "time": 0 },
            { "path": "1/51", "time": 488 },
            { "path": "1/58", "time": 549 },
            { "path": "1/146", "time": 1400 },
            { "path": "1/51/356", "time": 2648 },
            { "path": "1/51/356/571", "time": 3743 },
            { "path": "1/104793", "time": 31502 }
        ]
    }
]
```

## Field Breakdown
- **`cascade_id`**: A unique identifier for the citation cascade.
- **`original_user_id`**: The ID of the original user (or paper) initiating the cascade.
- **`timestamp`**: The Unix timestamp of the original event’s occurrence.
- **`number_of_participants`**: The total number of participants involved in the cascade.
- **`participants`**: A list of events representing how the information was shared:
  - **`path`**: The sequence of users involved in the propagation.
  - **`time`**: The number of seconds after the original event when the citation occurred.

## Understanding the Cascade Flow
The citation cascade represents how information spreads through direct and intermediary citations.

### Example Participants List Breakdown:

```json
"participants": [
    { "path": "1", "time": 0 },
    { "path": "1/51", "time": 488 },
    { "path": "1/58", "time": 549 },
    { "path": "1/146", "time": 1400 },
    { "path": "1/51/356", "time": 2648 },
    { "path": "1/51/356/571", "time": 3743 },
    { "path": "1/104793", "time": 31502 }
]
```

- **User `1` (Original event)** → The cascade starts with user `1` at `time = 0`.
- **User `51`** → Cites user `1` **488 seconds** after the original event (`1 → 51`).
- **User `58`** → Directly cites user `1` **549 seconds** after (`1 → 58`).
- **User `146`** → Cites user `1` after **1400 seconds** (`1 → 146`).
- **User `356`** → Cites user `1`, but through `51` **2648 seconds** later (`1 → 51 → 356`).
- **User `571`** → Cites user `1`, but through `51` and `356` **3743 seconds** later (`1 → 51 → 356 → 571`).
- **User `104793`** → Directly cites user `1` after **31,502 seconds** (`1 → 104793`).

## Explaining the Propagation Path
Each participant in the cascade follows a structured path:
- **Direct Citation**: If the path contains only two elements (`original_user_id/new_user_id`), the citation was direct.
- **Intermediary Citation**: If the path contains multiple elements (`original_user_id/intermediary_user_id/new_user_id`), the information was shared indirectly through intermediary citations.

### Example Breakdown:

```json
"path": "1/51/356", "time": 2648
```

- User `356` received the information **via** user `51`, who originally received it from user `1`.
- This means user `356` did **not** cite user `1` directly but rather found the information through an intermediary (`51`).
- The time `2648` means user `356` cited user `1` **2648 seconds after the original event**.

This hierarchical format allows for **tracking how information spreads** in a citation network over time.

## Usage & Applications
This JSON dataset can be used for:
- **Scientific citation analysis**: Identifying influential papers and citation patterns.
- **Network propagation modeling**: Studying how information spreads in academic research.
- **Machine learning applications**: Training models for citation prediction and trend analysis.

By providing a structured format, the JSON conversion allows for efficient querying and visualization of citation trends over time.
