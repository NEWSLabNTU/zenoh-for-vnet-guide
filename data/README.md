# Remote Driving Message Characteristics

## Message Characteristic

According to several papers and research, we have summarized four types of messages that most commonly appear in remote driving cases. Considering the different hardware devices involved and their varying functions, the characteristics of different types of information also vary significantly.

- Control Messages
    - Message Size: Typically small (e.g., a few bytes to tens of bytes), as it often includes control commands or instructions.
    - Message Rate: High frequency, usually sent multiple times per second (e.g., 10-100 msg/s) to ensure real-time control.
    - Latency Sensitivity: Extremely low latency required, as delayed control messages could result in unsafe operations.
    - Reliability Requirement: High reliability to avoid control errors.
- Camera Feed
    - Message Size: Large, as each message might contain image or video data. Size can range from kilobytes (KB) to megabytes (MB), depending on resolution and compression.
    - Message Rate: Moderate to high frequency, depending on the frame rate (e.g., 15-60 frames per second, each frame being one message).
    - Latency Sensitivity: Moderate latency tolerance, though real-time feedback is still important.
    - Reliability Requirement: Moderate to high reliability, as missing frames may degrade video quality but not disrupt overall system functionality.
- Point Cloud Data
    - Message Size: Very large, as point cloud data contains 3D spatial coordinates. Size can range from hundreds of kilobytes (KB) to several megabytes (MB) per message.
    - Message Rate: Lower frequency, typically a few messages per second (e.g., 1-10 msg/s) depending on the system’s sensor capture rate.
    - Latency Sensitivity: Moderate, as point cloud data is often used for mapping or object detection.
    - Reliability Requirement: High reliability needed for accurate environmental mapping and object recognition.
- Vehicle Status Updates
    - Message Size: Small (e.g., a few bytes), as it typically includes parameters such as speed, acceleration, and fuel levels.
    - Message Rate: High frequency, sent multiple times per second (e.g., 10-50 msg/s) for real-time monitoring of the vehicle's condition.
    - Latency Sensitivity: Low latency required to ensure that the system has up-to-date information about the vehicle’s status.
    - Reliability Requirement: High reliability to avoid inaccurate status reporting.

## Input Data Table

Through the information mentioned above, we can list the characteristics of various types of information in the following table...

| Type | Min Bits/s rate | Production Interval (ms) | Payload Size (Bytes) |
| :-----| ----: | :----: | :----: |
| Control | 1K | 100 | 128 |
| Camera | 4M | 33.33 | 1K |
| Point Cloud / Proceed Data | 16M | 100 | 1K |
| Camera | 5K | 100 | 128 |


| Type | Delay Constraint (D<sub>i</sub>) | Reliability Constraint (R<sub>i</sub>) |
| :-----| ----: | :----: |
| Control | 50 | 99.99% |
| Camera | 100 | 99% |
| Point Cloud / Proceed Data | 200 | 99.9% |
| Status | 100 | 99% |


## Mesage Constraint Sorting

- Latency Sensitivity Sorting :

    L<sub>control</sub> < L<sub>status</sub> <= L<sub>camera</sub> < L<sub>pointcloud</sub>

    - **Control message** require the lowest latency because they directly affect vehicle control and safety.

    - **Vehicle status** updates also need low latency to ensure real-time monitoring, but not as critical as control 

    - **Camera feed** can tolerate some delay as visual feedback doesn't require immediate response like control commands.

    - **Point cloud data** has the least stringent latency requirement, as it is primarily used for environmental mapping and can handle slight delays.

- Reliability Requirement sorting :

    R<sub>control</sub> > R<sub>pointcloud</sub> > R<sub>status</sub> >= R<sub>camera</sub>

    - **Control messages** must have the highest reliability since errors in control can lead to unsafe conditions.

    - **Vehicle status** updates require reliable transmission to ensure accurate information on the vehicle's condition, but a slightly lower priority than point cloud data.

    - **Camera feed** can tolerate some level of unreliability, such as frame drops, without severely affecting system performance, making it the least demanding in terms of reliability.

    - **Point cloud data** needs high reliability for accurate 3D mapping and object detection.


## References 

[1] 3GPP TR 26.985 version 16.0.0 Release 16, ETSI standard, 2020

[2] Oren Musicant, Assaf Botzer, Shraga Shoval, Effects of simulated time delay on teleoperators’ performance in
inter-urban conditions, 2023

[3] Grigorios Kakkavas, Kwame Nseboah Nyarko, Teleoperated Support for Remote Driving over 5G Mobile Communications, IEEE MeditCom, 2022