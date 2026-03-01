// API client for Runtime Rush backend

// ✅ Use Railway backend in production, localhost in development
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  "https://runtime-rush-production.up.railway.app";

export interface Challenge {
  id: string;
  title: string;
  description: string;
  language: string;
  level?: number;
  fragments: CodeFragment[];
  correct_solution: string;
  test_cases: TestCase[];
  start_time: string;
  end_time: string;
  created_by: string;
}

export interface CodeFragment {
  id: string;
  content: string;
  order: number;
}

export interface TestCase {
  id: string;
  input: string;
  expected_output: string;
  visible: boolean;
}

export interface Submission {
  id: string;
  challenge_id: string;
  participant_id: string;
  code: string;
  timestamp: string;
  is_correct: boolean;
  validation_result: ValidationResult;
}

export interface ValidationResult {
  is_valid: boolean;
  syntax_errors: any[];
  test_results: TestResult[];
  all_tests_passed: boolean;
}

export interface TestResult {
  test_case_id: string;
  passed: boolean;
  actual_output: string;
  expected_output: string;
  execution_time: number;
  error?: string;
}

export interface UserRegister {
  username: string;
  email: string;
  password: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserResponse {
  id: string;
  username: string;
  email: string;
  role: string;
  current_level: number;
}

export interface UserProgress {
  user_id: string;
  current_level: number;
  level1_completed: boolean;
  level2_completed: boolean;
  level3_completed: boolean;
  total_score: number;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  // ================= AUTH =================

  async register(userData: UserRegister): Promise<UserResponse> {
    const response = await fetch(`${this.baseUrl}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Registration failed");
    }
    return response.json();
  }

  async login(credentials: UserLogin): Promise<UserResponse> {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Login failed");
    }
    return response.json();
  }

  async getUserProgress(userId: string): Promise<UserProgress> {
    const response = await fetch(
      `${this.baseUrl}/api/auth/users/${userId}/progress`
    );
    if (!response.ok) throw new Error("Failed to fetch user progress");
    return response.json();
  }

  async completeLevel(
    userId: string,
    level: number,
    timeTaken: number = 300
  ): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/auth/users/${userId}/complete-level/${level}?time_taken=${timeTaken}`,
      { method: "POST" }
    );

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to complete level");
    }
    return response.json();
  }

  // ================= ADMIN =================

  async getAllUsers(adminId: string): Promise<any[]> {
    const response = await fetch(
      `${this.baseUrl}/api/admin/users?admin_id=${adminId}`
    );
    if (!response.ok) throw new Error("Failed to fetch users");
    return response.json();
  }

  async getChallengesByLevel(level: number, adminId: string): Promise<any[]> {
    const response = await fetch(
      `${this.baseUrl}/api/admin/challenges/by-level/${level}?admin_id=${adminId}`
    );
    if (!response.ok) throw new Error("Failed to fetch challenges");
    return response.json();
  }

  async deleteChallenge(challengeId: string, adminId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/admin/challenges/${challengeId}?admin_id=${adminId}`,
      { method: "DELETE" }
    );
    if (!response.ok) throw new Error("Failed to delete challenge");
    return response.json();
  }

  async getAdminStats(adminId: string): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/admin/stats?admin_id=${adminId}`
    );
    if (!response.ok) throw new Error("Failed to fetch stats");
    return response.json();
  }

  async createAdmin(
    username: string,
    email: string,
    password: string
  ): Promise<any> {
    const response = await fetch(
      `${this.baseUrl}/api/admin/create-admin?username=${username}&email=${email}&password=${password}`,
      { method: "POST" }
    );
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to create admin");
    }
    return response.json();
  }

  // ================= CHALLENGES =================

  async getChallenges(): Promise<Challenge[]> {
    const response = await fetch(`${this.baseUrl}/api/challenges`);
    if (!response.ok) throw new Error("Failed to fetch challenges");
    return response.json();
  }

  async getChallenge(id: string): Promise<Challenge> {
    const response = await fetch(`${this.baseUrl}/api/challenges/${id}`);
    if (!response.ok) throw new Error("Failed to fetch challenge");
    return response.json();
  }

  async createChallenge(challenge: Partial<Challenge>): Promise<Challenge> {
    const response = await fetch(`${this.baseUrl}/api/challenges`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(challenge),
    });
    if (!response.ok) throw new Error("Failed to create challenge");
    return response.json();
  }

  // ================= SUBMISSIONS =================

  async submitCode(
    challengeId: string,
    participantId: string,
    code: string
  ): Promise<Submission> {
    const response = await fetch(`${this.baseUrl}/api/submissions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        challenge_id: challengeId,
        participant_id: participantId,
        code,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to submit code");
    }
    return response.json();
  }

  async getSubmission(id: string): Promise<Submission> {
    const response = await fetch(`${this.baseUrl}/api/submissions/${id}`);
    if (!response.ok) throw new Error("Failed to fetch submission");
    return response.json();
  }

  async getSubmissionsByChallenge(
    challengeId: string
  ): Promise<Submission[]> {
    const response = await fetch(
      `${this.baseUrl}/api/submissions/challenge/${challengeId}`
    );
    if (!response.ok) throw new Error("Failed to fetch submissions");
    return response.json();
  }

  async getSubmissionsByParticipant(
    participantId: string
  ): Promise<Submission[]> {
    const response = await fetch(
      `${this.baseUrl}/api/submissions/participant/${participantId}`
    );
    if (!response.ok) throw new Error("Failed to fetch submissions");
    return response.json();
  }

  async getLeaderboard(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/auth/leaderboard`);
    if (!response.ok) throw new Error("Failed to fetch leaderboard");
    return response.json();
  }
}

export const apiClient = new ApiClient();