# Implementation Plan: Runtime Rush Platform

## Overview

This implementation plan breaks down the Runtime Rush platform into discrete coding tasks using Python for the backend (FastAPI), React for the frontend, PostgreSQL for data persistence, Redis for caching, and Docker for code execution sandboxing. The plan follows an incremental approach where each task builds on previous work, with property-based tests integrated throughout to validate correctness early.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - Create Python backend project with FastAPI, SQLAlchemy, Redis client
  - Set up PostgreSQL database with schema from design document
  - Create React frontend project with TypeScript, Monaco Editor
  - Configure Docker for sandbox execution environment
  - Set up pytest with pytest-asyncio for testing
  - Install hypothesis for property-based testing in Python
  - _Requirements: All requirements (infrastructure foundation)_

- [x] 2. Implement data models and database layer
  - [x] 2.1 Create SQLAlchemy models for all database tables
    - Implement User, Challenge, CodeFragment, TestCase, Submission, Winner, ParticipantSession models
    - Define relationships and constraints
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 6.1, 6.2, 6.3, 6.4, 7.1, 10.1, 10.2_
  
  - [x] 2.2 Write property test for challenge data round-trip persistence
    - **Property 1: Challenge Data Round-Trip Persistence**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.5, 2.1**
  
  - [x] 2.3 Write property test for submission round-trip persistence
    - **Property 15: Submission Round-Trip Persistence**
    - **Validates: Requirements 6.1, 6.2, 6.3, 6.4**
  
  - [x] 2.4 Write property test for session round-trip persistence
    - **Property 5: Session Code Round-Trip Persistence**
    - **Validates: Requirements 3.4, 10.2**

- [x] 3. Implement Challenge Manager
  - [x] 3.1 Create ChallengeManager class with CRUD operations
    - Implement createChallenge, getChallenge, updateChallenge, deleteChallenge, listChallenges
    - Add challenge validation logic for required fields
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7_
  
  - [x] 3.2 Write property test for challenge validation
    - **Property 2: Challenge Validation Rejects Incomplete Data**
    - **Validates: Requirements 1.6**
  
  - [x] 3.3 Write unit tests for challenge CRUD edge cases
    - Test creating challenge with empty title
    - Test retrieving non-existent challenge
    - Test updating challenge with invalid data
    - _Requirements: 1.1, 1.6_

- [x] 4. Implement fragment scrambling and test case filtering
  - [x] 4.1 Add fragment scrambling logic to challenge retrieval
    - Implement randomization of fragment order when retrieving for participants
    - Preserve original order in database
    - _Requirements: 2.2_
  
  - [x] 4.2 Add test case visibility filtering
    - Filter expected outputs from visible test cases
    - Exclude hidden test cases from participant view
    - _Requirements: 2.5_
  
  - [x] 4.3 Write property test for fragment scrambling
    - **Property 3: Fragment Scrambling**
    - **Validates: Requirements 2.2**
  
  - [x] 4.4 Write property test for test case visibility filtering
    - **Property 4: Test Case Input Visibility Filtering**
    - **Validates: Requirements 2.5**

- [x] 5. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement Sandbox Orchestrator
  - [ ] 6.1 Create SandboxOrchestrator class with Docker integration
    - Implement execute method that spawns Docker containers
    - Configure resource limits (CPU, memory, time, network isolation)
    - Capture stdout, stderr, exit code
    - Implement container cleanup logic
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_
  
  - [ ] 6.2 Write property test for code execution output capture
    - **Property 6: Code Execution Returns Output**
    - **Validates: Requirements 4.1, 4.6**
  
  - [ ] 6.3 Write property test for file system access restriction
    - **Property 7: File System Access Restriction**
    - **Validates: Requirements 4.2**
  
  - [ ] 6.4 Write property test for network access restriction
    - **Property 8: Network Access Restriction**
    - **Validates: Requirements 4.3**
  
  - [ ] 6.5 Write unit tests for timeout and memory limit enforcement
    - Test code that runs longer than 10 seconds times out
    - Test code that allocates more than 256MB is terminated
    - _Requirements: 4.4, 4.5, 4.7, 4.8_

- [ ] 7. Implement syntax checking and validation
  - [ ] 7.1 Create syntax checker for Python code
    - Use Python's ast module to parse and detect syntax errors
    - Return line, column, and error message for syntax errors
    - _Requirements: 5.1, 9.4_
  
  - [ ] 7.2 Write property test for syntax error detection
    - **Property 9: Syntax Error Detection**
    - **Validates: Requirements 5.1, 9.4**

- [ ] 8. Implement Validation Manager
  - [ ] 8.1 Create ValidationManager class with test case execution
    - Implement validateSubmission method
    - Implement checkSyntax method
    - Implement runTestCases method that uses SandboxOrchestrator
    - Add output comparison logic with trailing whitespace normalization
    - Determine submission correctness based on all tests passing
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_
  
  - [ ] 8.2 Write property test for syntax errors preventing test execution
    - **Property 10: Syntax Errors Prevent Test Execution**
    - **Validates: Requirements 5.2**
  
  - [ ] 8.3 Write property test for all test cases executing
    - **Property 11: All Test Cases Execute**
    - **Validates: Requirements 5.3, 11.1**
  
  - [ ] 8.4 Write property test for output comparison correctness
    - **Property 12: Output Comparison Correctness**
    - **Validates: Requirements 5.4, 5.7**
  
  - [ ] 8.5 Write property test for submission correctness determination
    - **Property 13: Submission Correctness Determination**
    - **Validates: Requirements 5.5**
  
  - [ ] 8.6 Write property test for test results including pass/fail status
    - **Property 14: Test Results Include Pass/Fail Status**
    - **Validates: Requirements 5.6, 11.2**

- [ ] 9. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Implement Submission Manager
  - [x] 10.1 Create SubmissionManager class with submission handling
    - Implement submitCode method with server-side timestamp
    - Implement getSubmission, getSubmissionsByParticipant, getSubmissionsByChallenge
    - Add validation to reject submissions after challenge end time
    - Integrate with ValidationManager for automatic validation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  
  - [x] 10.2 Write property test for multiple submissions allowed
    - **Property 16: Multiple Submissions Allowed**
    - **Validates: Requirements 6.5**
  
  - [x] 10.3 Write property test for submissions rejected after challenge end
    - **Property 17: Submissions Rejected After Challenge End**
    - **Validates: Requirements 6.6**

- [x] 11. Implement Winner Manager
  - [x] 11.1 Create WinnerManager class with winner declaration logic
    - Implement declareWinner with database transaction and SELECT FOR UPDATE
    - Implement getWinner method
    - Implement getLeaderboard method with chronological ordering
    - Ensure winner immutability through database constraints
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  
  - [x] 11.2 Write property test for first correct submission wins
    - **Property 18: First Correct Submission Wins**
    - **Validates: Requirements 7.1, 7.2**
  
  - [x] 11.3 Write property test for winner immutability
    - **Property 19: Winner Immutability**
    - **Validates: Requirements 7.4**
  
  - [x] 11.4 Write property test for leaderboard chronological ordering
    - **Property 20: Leaderboard Chronological Ordering**
    - **Validates: Requirements 7.5**

- [x] 12. Implement timer and challenge status logic
  - [x] 12.1 Create utility functions for time calculations
    - Implement calculateRemainingTime function
    - Implement calculateTimeUntilStart function
    - Implement isChallengeActive function
    - Implement markChallengeAsEnded function
    - _Requirements: 8.1, 8.3, 8.4, 8.5_
  
  - [x] 12.2 Write property test for remaining time calculation
    - **Property 21: Remaining Time Calculation**
    - **Validates: Requirements 8.1**
  
  - [x] 12.3 Write property test for challenge status transition
    - **Property 22: Challenge Status Transition at End Time**
    - **Validates: Requirements 8.3**
  
  - [x] 12.4 Write property test for time until start calculation
    - **Property 23: Time Until Start Calculation**
    - **Validates: Requirements 8.5**

- [x] 13. Implement Session Manager
  - [x] 13.1 Create SessionManager class with auto-save functionality
    - Implement saveSession method with upsert logic
    - Implement getSession method
    - Implement autoSave method
    - Add background task for periodic auto-save
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [x] 13.2 Write property test for session isolation
    - **Property 24: Session Isolation**
    - **Validates: Requirements 10.3**
  
  - [x] 13.3 Write property test for session persistence after challenge end
    - **Property 25: Session Persistence After Challenge End**
    - **Validates: Requirements 10.4**
  
  - [x] 13.4 Write unit test for auto-save timing
    - Test that auto-save triggers after 30 seconds
    - _Requirements: 10.1_

- [x] 14. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 15. Implement REST API endpoints
  - [x] 15.1 Create FastAPI routes for challenge management
    - POST /api/challenges - create challenge
    - GET /api/challenges/:id - get challenge
    - GET /api/challenges - list challenges
    - PUT /api/challenges/:id - update challenge
    - DELETE /api/challenges/:id - delete challenge
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7_
  
  - [x] 15.2 Create FastAPI routes for submissions
    - POST /api/challenges/:id/submit - submit code
    - GET /api/submissions/:id - get submission
    - GET /api/challenges/:id/submissions - get challenge submissions
    - GET /api/participants/:id/submissions - get participant submissions
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_
  
  - [x] 15.3 Create FastAPI routes for test execution
    - POST /api/challenges/:id/test - run code against visible test cases
    - _Requirements: 11.1, 11.2, 11.3, 11.5_
  
  - [x] 15.4 Create FastAPI routes for winners and leaderboard
    - GET /api/challenges/:id/winner - get winner
    - GET /api/challenges/:id/leaderboard - get leaderboard
    - _Requirements: 7.3, 7.5_
  
  - [x] 15.5 Create FastAPI routes for session management
    - POST /api/sessions - save session
    - GET /api/sessions/:participantId/:challengeId - get session
    - _Requirements: 10.1, 10.2, 10.3, 10.4_
  
  - [x] 15.6 Write integration tests for API endpoints
    - Test authentication and authorization
    - Test error responses and status codes
    - Test request validation
    - _Requirements: All API-related requirements_

- [x] 16. Implement WebSocket server for real-time updates
  - [x] 16.1 Create WebSocket endpoint for timer updates
    - Broadcast remaining time every second to connected clients
    - Send challenge status updates (started, ended)
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [x] 16.2 Create WebSocket endpoint for winner announcements
    - Broadcast winner declaration to all participants
    - _Requirements: 7.2, 7.3_

- [ ] 17. Implement security and isolation features
  - [ ] 17.1 Add sandbox security restrictions
    - Configure Docker to block environment variable access
    - Configure Docker to prevent process spawning
    - Configure Docker to prevent system modifications
    - Add malicious code pattern detection
    - _Requirements: 12.1, 12.2, 12.3, 12.4_
  
  - [ ] 17.2 Add execution audit logging
    - Log all code execution attempts with participant, challenge, timestamp
    - Store logs in database or log aggregation system
    - _Requirements: 12.5_
  
  - [ ] 17.3 Write property test for environment variable isolation
    - **Property 27: Environment Variable Isolation**
    - **Validates: Requirements 12.1**
  
  - [ ] 17.4 Write property test for process spawning prevention
    - **Property 28: Process Spawning Prevention**
    - **Validates: Requirements 12.2**
  
  - [ ] 17.5 Write property test for system modification prevention
    - **Property 29: System Modification Prevention**
    - **Validates: Requirements 12.3**
  
  - [ ] 17.6 Write property test for malicious code termination
    - **Property 30: Malicious Code Termination**
    - **Validates: Requirements 12.4**
  
  - [ ] 17.7 Write property test for execution audit logging
    - **Property 31: Execution Audit Logging**
    - **Validates: Requirements 12.5**

- [ ] 18. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 19. Implement React frontend components
  - [x] 19.1 Create challenge list and detail views
    - Display available challenges
    - Show challenge description, language, start/end times
    - _Requirements: 2.3, 2.4, 8.4_
  
  - [x] 19.2 Create code editor component with Monaco Editor
    - Integrate Monaco Editor with syntax highlighting
    - Display code fragments
    - Allow code editing with line numbers
    - _Requirements: 2.1, 3.1, 3.2, 3.3, 3.5_
  
  - [x] 19.3 Create timer component
    - Display countdown timer with real-time updates via WebSocket
    - Show time until start or remaining time
    - _Requirements: 8.1, 8.2, 8.5_
  
  - [x] 19.4 Create submission and validation UI
    - Add submit button
    - Display validation results (syntax errors, test results)
    - Show pass/fail status for each test case
    - _Requirements: 5.6, 6.1, 11.2, 11.3_
  
  - [x] 19.5 Create winner announcement component
    - Display winner information when declared
    - Show leaderboard of correct submissions
    - _Requirements: 7.3, 7.5_
  
  - [x] 19.6 Create organizer challenge creation form
    - Form for creating challenges with all required fields
    - Interface for defining fragments and test cases
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 1.6, 1.7_

- [x] 20. Implement frontend-backend integration
  - [x] 20.1 Create API client service in React
    - Implement fetch calls to all backend endpoints
    - Handle authentication tokens
    - Handle error responses
    - _Requirements: All requirements (integration layer)_
  
  - [x] 20.2 Implement WebSocket client in React
    - Connect to WebSocket server
    - Handle timer updates
    - Handle winner announcements
    - _Requirements: 8.1, 8.2, 7.2, 7.3_
  
  - [x] 20.3 Implement auto-save functionality in editor
    - Trigger auto-save every 30 seconds
    - Save code to backend via API
    - Restore code on page load
    - _Requirements: 10.1, 10.2_

- [x] 21. Implement test case execution feature
  - [x] 21.1 Add "Run Tests" button to UI
    - Call test execution API endpoint
    - Display actual outputs for each test case
    - Show pass/fail indicators
    - _Requirements: 11.1, 11.2, 11.3_
  
  - [x] 21.2 Write property test for unlimited test executions
    - **Property 26: Unlimited Test Executions**
    - **Validates: Requirements 11.5**

- [x] 22. Final checkpoint and integration testing
  - [x] 22.1 Run all property-based tests
    - Verify all 31 properties pass with 100+ iterations
    - _Requirements: All requirements_
  
  - [x] 22.2 Run all unit tests
    - Verify edge cases and error conditions
    - _Requirements: All requirements_
  
  - [x] 22.3 Perform end-to-end integration testing
    - Test complete workflow: challenge creation → participant coding → submission → winner declaration
    - Test with multiple concurrent participants
    - Test error scenarios and recovery
    - _Requirements: All requirements_

- [x] 23. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with 100+ randomized iterations
- Unit tests validate specific examples and edge cases
- The implementation uses Python (FastAPI) for backend, React for frontend, PostgreSQL for database, Redis for caching, and Docker for sandboxing
- Checkpoints ensure incremental validation throughout development
- Security and isolation are critical - sandbox configuration must be thoroughly tested
