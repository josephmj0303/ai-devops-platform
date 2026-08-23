import { useEffect, useState } from "react";

import {
  analyzeLogs,
  analyzeDockerfile,
  analyzeKubernetes,
  analyzeTerraform,
  getAnalysisHistory,
  getDockerContainers,
  getKubernetesDeployments,
  getAvailableActions,
  restartDockerContainer,
  restartKubernetesDeployment,
  getActionHistory,
  interpretAIAction,
} from "../api/ai";

import type {
  AnalysisSeverity,
  AIAnalysisHistoryItem,
  AnalysisType,
  DockerAnalysisResponse,
  KubernetesAnalysisResponse,
  TerraformAnalysisResponse,
  LogAnalysisResponse,
  DevOpsActionHistoryItem,
  AIActionInterpretResponse,
} from "../types/ai";

type AnalysisResult =
  | LogAnalysisResponse
  | DockerAnalysisResponse
  | KubernetesAnalysisResponse
  | TerraformAnalysisResponse;

const analysisLabels: Record<AnalysisType, string> = {
  logs: "Application Logs",
  dockerfile: "Dockerfile",
  kubernetes: "Kubernetes Manifest",
  terraform: "Terraform",
};

const placeholders: Record<AnalysisType, string> = {
  logs: `Paste application logs here...

Example:
ERROR: connection refused
database postgres:5432 is not reachable`,

  dockerfile: `Paste your Dockerfile here...

Example:
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]`,

  kubernetes: `Paste your Kubernetes manifest here...

Example:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app`,

  terraform: `Paste your Terraform configuration here...

Example:
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "app" {
  ...
}`,
};

function severityClass(severity: AnalysisSeverity): string {
  return `severity-${severity}`;
}

function AIAssistant() {
  const [analysisType, setAnalysisType] =
    useState<AnalysisType>("logs");

  const [input, setInput] = useState("");
  const [result, setResult] =
    useState<AnalysisResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [actionPrompt, setActionPrompt] = useState("");

  const [actionIntent, setActionIntent] =
    useState<AIActionInterpretResponse | null>(null);

  const [actionInterpretLoading, setActionInterpretLoading] =
    useState(false);

  const [actionInterpretError, setActionInterpretError] =
    useState("");
  
  const [history, setHistory] = useState<
    AIAnalysisHistoryItem[]
  >([]);

  const [historyLoading, setHistoryLoading] =
    useState(true);

  const [selectedHistory, setSelectedHistory] =
    useState<AIAnalysisHistoryItem | null>(null);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await getAnalysisHistory();
        setHistory(data);
      } catch (err) {
        console.error(
          "Failed to load AI analysis history:",
          err
        );
      } finally {
        setHistoryLoading(false);
      }
    };

    loadHistory();
  }, []);

  const handleAnalyze = async () => {
    if (!input.trim()) {
      setError("Please provide input for analysis.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      let response: AnalysisResult;

      switch (analysisType) {
        case "logs":
          response = await analyzeLogs(input);
          break;

        case "dockerfile":
          response = await analyzeDockerfile(input);
          break;

        case "kubernetes":
          response = await analyzeKubernetes(input);
          break;

        case "terraform":
          response = await analyzeTerraform(input);
          break;
      }

      setResult(response);

      const updatedHistory =
        await getAnalysisHistory();

      setHistory(updatedHistory);
    } catch (err) {
      console.error("AI analysis failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleTypeChange = (
    type: AnalysisType
  ) => {
    setAnalysisType(type);
    setInput("");
    setResult(null);
    setError("");
  };

  const handleInterpretAction = async () => {
    if (!actionPrompt.trim()) {
      setActionInterpretError(
        "Please describe the DevOps action you want AI to perform."
      );
      return;
    }

    setActionInterpretLoading(true);
    setActionInterpretError("");
    setActionIntent(null);

    try {
      const response = await interpretAIAction(
        actionPrompt
      );

      setActionIntent(response);
    } catch (err) {
      console.error(
        "AI action interpretation failed:",
        err
      );

      setActionInterpretError(
        "Failed to interpret the DevOps action."
      );
    } finally {
      setActionInterpretLoading(false);
    }
  };

  return (
    <div className="ai-page">
      <div className="ai-header">
        <div>
          <h1>AI DevOps Assistant</h1>

          <p>
            Analyze DevOps configurations, infrastructure,
            and application logs using AI.
          </p>
        </div>
      </div>

      <div className="ai-console">
        <div className="ai-controls">
          <label htmlFor="analysis-type">
            Analysis Type
          </label>

          <select
            id="analysis-type"
            value={analysisType}
            onChange={(event) =>
              handleTypeChange(
                event.target.value as AnalysisType
              )
            }
          >
            <option value="logs">
              Application Logs
            </option>

            <option value="dockerfile">
              Dockerfile
            </option>

            <option value="kubernetes">
              Kubernetes Manifest
            </option>

            <option value="terraform">
              Terraform
            </option>
          </select>
        </div>

        <div className="ai-input-section">
          <label htmlFor="ai-input">
            {analysisLabels[analysisType]}
          </label>

          <textarea
            id="ai-input"
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            placeholder={placeholders[analysisType]}
            rows={16}
          />
        </div>

        <div className="ai-result-section ai-devops-actions">
          <h2>AI DevOps Actions</h2>

          <p>
            Describe a DevOps action in natural language.
            AI will identify the supported action before
            execution.
          </p>

          <textarea
            value={actionPrompt}
            onChange={(event) =>
              setActionPrompt(event.target.value)
            }
            placeholder="Example: Restart the ingress-nginx-controller deployment in the ingress-nginx namespace"
            rows={4}
            disabled={actionInterpretLoading}
          />

          {actionInterpretError && (
            <div className="ai-action-error">
              {actionInterpretError}
            </div>
          )}

          <button
            type="button"
            className="ai-action-button"
            onClick={handleInterpretAction}
            disabled={actionInterpretLoading}
          >
            {actionInterpretLoading
              ? "Interpreting..."
              : "Interpret with AI"}
          </button>

          {actionIntent && (
            <div className="ai-action-card">
              <div className="ai-action-info">
                <strong>
                  AI Action Preview
                </strong>

                <p>
                  {actionIntent.reason}
                </p>

                {actionIntent.is_action ? (
                  <>
                    <p>
                      <strong>Action:</strong>{" "}
                      {actionIntent.action}
                    </p>

                    <p>
                      <strong>Target:</strong>{" "}
                      {actionIntent.target}
                    </p>

                    {actionIntent.namespace && (
                      <p>
                        <strong>Namespace:</strong>{" "}
                        {actionIntent.namespace}
                      </p>
                    )}
                  </>
                ) : (
                  <p>
                    No executable DevOps action was identified.
                  </p>
                )}
              </div>
            </div>
          )}
        </div> 

        {error && (
          <div className="ai-error">
            {error}
          </div>
        )}

        <button
          className="ai-analyze-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze with AI"}
        </button>
      </div>

      {result && (
        <AnalysisResultCard result={result} />
      )}

      <div className="ai-history">
        <div className="ai-history-header">
          <h2>Analysis History</h2>
          <span>
            {history.length} analyses
          </span>
        </div>

        {historyLoading ? (
          <p className="ai-history-empty">
            Loading history...
          </p>
        ) : history.length === 0 ? (
          <p className="ai-history-empty">
            No analysis history yet.
          </p>
        ) : (
          <>
            <div className="ai-history-list">
              {history.map((item) => (
                <div
                  className={`ai-history-item ${
                    selectedHistory?.id === item.id
                      ? "selected"
                      : ""
                  }`}
                  key={item.id}
                  onClick={() =>
                    setSelectedHistory(item)
                  }
                >
                  <button
                    type="button"
                    className="ai-history-view-button"
                    onClick={(event) => {
                      event.stopPropagation();
                      setSelectedHistory(item);
                    }}
                  >
                    View
                  </button>

                  <div className="ai-history-main">
                    <div className="ai-history-title">
                      {
                        analysisLabels[
                          item.analysis_type
                        ]
                      }
                    </div>

                    <div className="ai-history-summary">
                      {item.result.summary}
                    </div>

                    <div className="ai-history-meta">
                      <span>
                        {item.result.component}
                      </span>

                      <span>•</span>

                      <span>
                        {new Date(
                          item.created_at
                        ).toLocaleString()}
                      </span>
                    </div>
                  </div>

                  <span
                    className={`severity-badge ${severityClass(
                      item.result.severity
                    )}`}
                  >
                    {item.result.severity.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>

            {selectedHistory && (
              <HistoryDetails
                analysis={selectedHistory}
                onClose={() =>
                  setSelectedHistory(null)
                }
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}

interface AnalysisResultCardProps {
  result: AnalysisResult;
}

function AnalysisResultCard({
  result,
}: AnalysisResultCardProps) {
  const isLogResult =
    "likely_cause" in result &&
    "impact" in result;

  return (
    <div className="ai-result">
      <div className="ai-result-header">
        <div>
          <h2>AI Analysis</h2>

          <span className="ai-component">
            {result.component}
          </span>
        </div>

        <span
          className={`severity-badge ${severityClass(
            result.severity
          )}`}
        >
          {result.severity.toUpperCase()}
        </span>
      </div>

      <div className="ai-result-section">
        <h3>Summary</h3>
        <p>{result.summary}</p>
      </div>

      {isLogResult ? (
        <>
          <div className="ai-result-section">
            <h3>Likely Cause</h3>
            <p>{result.likely_cause}</p>
          </div>

          <div className="ai-result-section">
            <h3>Impact</h3>
            <p>{result.impact}</p>
          </div>
        </>
      ) : (
        <div className="ai-result-section">
          <h3>Findings</h3>

          <ul>
            {result.findings?.map(
              (finding, index) => (
                <li key={index}>
                  {finding}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      <div className="ai-result-section">
        <h3>Recommended Actions</h3>

        <ul className="recommendations">
          {result.recommended_actions.map(
            (action, index) => (
              <li key={index}>
                <span className="checkmark">
                  ✓
                </span>

                <span>{action}</span>
              </li>
            )
          )}
        </ul>
      </div>
    </div>
  );
}

interface HistoryDetailsProps {
  analysis: AIAnalysisHistoryItem;
  onClose: () => void;
}

function HistoryDetails({
  analysis,
  onClose,
}: HistoryDetailsProps) {
  const result = analysis.result;

  const [containers, setContainers] =
    useState<
      {
        name: string;
        status: string;
        image: string;
      }[]
    >([]);

  const [deployments, setDeployments] = useState<
    {
      name: string;
      namespace: string;
      desired_replicas: number;
      ready_replicas: number;
      available_replicas: number;
    }[]
  >([]);

  const [selectedDeployment, setSelectedDeployment] =
    useState("");

  const [selectedContainer, setSelectedContainer] =
    useState("");

  const [actionLoading, setActionLoading] =
    useState(false);

  const [actionResult, setActionResult] =
    useState("");

  const [actionError, setActionError] =
    useState("");

  const [actionAvailable, setActionAvailable] =
    useState(false);

  const [actionHistory, setActionHistory] =
    useState<DevOpsActionHistoryItem[]>([]);

  /*
   * Load available DevOps actions and
   * current targets for the selected component.
   */
  useEffect(() => {
    const loadActions = async () => {
      try {
        if (result.component === "Docker") {
          const available =
            await getAvailableActions("Docker");

          const restartAvailable =
            available.actions.some(
              (action) =>
                action.action === "docker_restart" &&
                action.enabled
            );

          setActionAvailable(restartAvailable);

          if (restartAvailable) {
            const data =
              await getDockerContainers();

            setContainers(data);

            if (data.length > 0) {
              setSelectedContainer(
                data[0].name
              );
            }
          }

          return;
        }

        if (result.component === "Kubernetes") {
          const available =
            await getAvailableActions("Kubernetes");

          const restartAvailable =
            available.actions.some(
              (action) =>
                action.action ===
                  "kubernetes_restart_deployment" &&
                action.enabled
            );

          setActionAvailable(restartAvailable);

          if (restartAvailable) {
            const data =
              await getKubernetesDeployments();

            setDeployments(data);

            if (data.length > 0) {
              setSelectedDeployment(
                `${data[0].namespace}/${data[0].name}`
              );
            }
          }
        }
      } catch (err) {
        console.error(
          "Failed to load DevOps actions:",
          err
        );
      }
    };

    loadActions();
  }, [result.component]);

  /*
   * Load persisted action history
   * for the selected analysis.
   */
  useEffect(() => {
    const loadActionHistory =
      async () => {
        try {
          const history =
            await getActionHistory(
              analysis.id
            );

          setActionHistory(history);
        } catch (err) {
          console.error(
            "Failed to load action history:",
            err
          );
        }
      };

    loadActionHistory();
  }, [analysis.id]);

  /*
   * Execute Docker restart and
   * refresh action history afterwards.
   */
  const handleRestartContainer =
    async () => {
      if (!selectedContainer) {
        setActionError(
          "Please select a container."
        );
        return;
      }

      setActionLoading(true);
      setActionResult("");
      setActionError("");

      try {
        const response =
          await restartDockerContainer(
            analysis.id,
            selectedContainer
          );

        if (
          response.status === "completed"
        ) {
          setActionResult(
            response.message
          );
        } else {
          setActionError(
            response.message
          );
        }

        /*
         * Reload persisted history after
         * every action execution.
         */
        const updatedHistory =
          await getActionHistory(
            analysis.id
          );

        setActionHistory(
          updatedHistory
        );
      } catch (err) {
        console.error(
          "Docker action failed:",
          err
        );

        setActionError(
          "Failed to execute Docker action."
        );

        /*
         * Even if the API returns an error,
         * try to refresh the persisted history.
         */
        try {
          const updatedHistory =
            await getActionHistory(
              analysis.id
            );

          setActionHistory(
            updatedHistory
          );
        } catch (historyError) {
          console.error(
            "Failed to refresh action history:",
            historyError
          );
        }
      } finally {
        setActionLoading(false);
      }
    };

  const handleRestartDeployment = async () => {
    if (!selectedDeployment) {
      setActionError(
        "Please select a deployment."
      );
      return;
    }

    const [namespace, deploymentName] =
      selectedDeployment.split("/");

    setActionLoading(true);
    setActionResult("");
    setActionError("");

    try {
      const response =
        await restartKubernetesDeployment(
          analysis.id,
          namespace,
          deploymentName
        );

      if (response.status === "completed") {
        setActionResult(response.message);
      } else {
        setActionError(response.message);
      }

      const updatedHistory =
        await getActionHistory(
          analysis.id
        );

      setActionHistory(updatedHistory);
    } catch (err) {
      console.error(
        "Kubernetes action failed:",
        err
      );

      setActionError(
        "Failed to execute Kubernetes action."
      );

      try {
        const updatedHistory =
          await getActionHistory(
            analysis.id
          );

        setActionHistory(
          updatedHistory
        );
      } catch (historyError) {
        console.error(
          "Failed to refresh action history:",
          historyError
        );
      }
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="ai-history-details">
      <div className="ai-history-details-header">
        <div>
          <h2>Analysis Details</h2>

          <div className="ai-history-details-meta">
            <span>
              {
                analysisLabels[
                  analysis.analysis_type
                ]
              }
            </span>

            <span>•</span>

            <span>
              {new Date(
                analysis.created_at
              ).toLocaleString()}
            </span>
          </div>
        </div>

        <button
          type="button"
          className="ai-history-close-button"
          onClick={onClose}
        >
          Close
        </button>
      </div>

      <div className="ai-history-details-status">
        <span>
          Component:{" "}
          <strong>
            {result.component}
          </strong>
        </span>

        <span
          className={`severity-badge ${severityClass(
            result.severity
          )}`}
        >
          {result.severity.toUpperCase()}
        </span>
      </div>

      <div className="ai-result-section">
        <h3>Summary</h3>
        <p>{result.summary}</p>
      </div>

      <div className="ai-result-section">
        <h3>Original Input</h3>

        <pre className="ai-history-input">
          {analysis.input_text}
        </pre>
      </div>

      {result.likely_cause && (
        <div className="ai-result-section">
          <h3>Likely Cause</h3>
          <p>{result.likely_cause}</p>
        </div>
      )}

      {result.impact && (
        <div className="ai-result-section">
          <h3>Impact</h3>
          <p>{result.impact}</p>
        </div>
      )}

      {result.findings &&
        result.findings.length > 0 && (
          <div className="ai-result-section">
            <h3>Findings</h3>

            <ul>
              {result.findings.map(
                (finding, index) => (
                  <li key={index}>
                    {finding}
                  </li>
                )
              )}
            </ul>
          </div>
        )}

      <div className="ai-result-section">
        <h3>Recommended Actions</h3>

        <ul className="recommendations">
          {result.recommended_actions.map(
            (action, index) => (
              <li key={index}>
                <span className="checkmark">
                  ✓
                </span>

                <span>{action}</span>
              </li>
            )
          )}
        </ul>
      </div>

      {result.component === "Docker" && (
        <div className="ai-result-section ai-devops-actions">
          <h3>DevOps Actions</h3>

          {!actionAvailable ? (
            <p>
              No executable Docker actions are
              currently available.
            </p>
          ) : (
            <>
              <div className="ai-action-card">
                <div className="ai-action-info">
                  <strong>
                    Restart Docker Container
                  </strong>

                  <p>
                    Restart a selected running
                    Docker container.
                  </p>
                </div>

                <div className="ai-action-controls">
                  <label htmlFor="docker-container">
                    Target Container
                  </label>

                  <select
                    id="docker-container"
                    value={selectedContainer}
                    onChange={(event) =>
                      setSelectedContainer(
                        event.target.value
                      )
                    }
                    disabled={actionLoading}
                  >
                    {containers.map(
                      (container) => (
                        <option
                          key={container.name}
                          value={container.name}
                        >
                          {container.name}
                        </option>
                      )
                    )}
                  </select>

                  <button
                    type="button"
                    className="ai-action-button"
                    onClick={
                      handleRestartContainer
                    }
                    disabled={
                      actionLoading ||
                      !selectedContainer
                    }
                  >
                    {actionLoading
                      ? "Executing..."
                      : "Execute Action"}
                  </button>
                </div>
              </div>

              {actionResult && (
                <div className="ai-action-success">
                  {actionResult}
                </div>
              )}

              {actionError && (
                <div className="ai-action-error">
                  {actionError}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {result.component === "Kubernetes" && (
        <div className="ai-result-section ai-devops-actions">
          <h3>DevOps Actions</h3>

          {!actionAvailable ? (
            <p>
              No executable Kubernetes actions are
              currently available.
            </p>
          ) : (
            <>
              <div className="ai-action-card">
                <div className="ai-action-info">
                  <strong>
                    Restart Kubernetes Deployment
                  </strong>

                  <p>
                    Restart a selected Kubernetes
                    deployment.
                  </p>
                </div>

                <div className="ai-action-controls">
                  <label htmlFor="kubernetes-deployment">
                    Target Deployment
                  </label>

                  <select
                    id="kubernetes-deployment"
                    value={selectedDeployment}
                    onChange={(event) =>
                      setSelectedDeployment(
                        event.target.value
                      )
                    }
                    disabled={actionLoading}
                  >
                    {deployments.map(
                      (deployment) => (
                        <option
                          key={`${deployment.namespace}/${deployment.name}`}
                          value={`${deployment.namespace}/${deployment.name}`}
                        >
                          {deployment.namespace}/
                          {deployment.name}
                        </option>
                      )
                    )}
                  </select>

                  <button
                    type="button"
                    className="ai-action-button"
                    onClick={
                      handleRestartDeployment
                    }
                    disabled={
                      actionLoading ||
                      !selectedDeployment
                    }
                  >
                    {actionLoading
                      ? "Executing..."
                      : "Execute Action"}
                  </button>
                </div>
              </div>

              {actionResult && (
                <div className="ai-action-success">
                  {actionResult}
                </div>
              )}

              {actionError && (
                <div className="ai-action-error">
                  {actionError}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {actionHistory.length > 0 && (
        <div className="ai-result-section ai-action-history">
          <h3>Action History</h3>

          <div className="action-history-list">
            {actionHistory.map(
              (item) => (
                <div
                  key={item.id}
                  className="action-history-item"
                >
                  <div className="action-history-header">
                    <strong>
                      {item.action ===
                      "docker_restart"
                        ? "Restart Docker Container"
                        : item.action}
                    </strong>

                    <span
                      className={`action-status ${item.status}`}
                    >
                      {item.status}
                    </span>
                  </div>

                  <div className="action-history-details">
                    <span>
                      <strong>
                        Target:
                      </strong>{" "}
                      {item.target}
                    </span>

                    <span>
                      <strong>
                        Executed:
                      </strong>{" "}
                      {new Date(
                        item.created_at
                      ).toLocaleString()}
                    </span>
                  </div>

                  <p>
                    {item.message}
                  </p>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default AIAssistant;
