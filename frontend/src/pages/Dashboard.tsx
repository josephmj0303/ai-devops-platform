import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getProjects } from "../api/projects";
import type { Project } from "../types/project";

export default function Dashboard() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProjects = async () => {
      try {
        const data = await getProjects();
        setProjects(data);
      } catch (error) {
        console.error("Failed to load projects:", error);
      } finally {
        setLoading(false);
      }
    };

    loadProjects();
  }, []);

  const recentProjects = [...projects]
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() -
        new Date(a.created_at).getTime()
    )
    .slice(0, 3);

  return (
    <div className="max-w-6xl mx-auto">

      {/* Header */}

      <div className="mb-8">
        <h1 className="text-4xl font-bold">
          Dashboard
        </h1>

        <p className="text-gray-600 mt-2">
          AI-powered DevOps workspace
        </p>
      </div>

      {/* Stats */}

      <div className="grid md:grid-cols-3 gap-6 mb-8">

        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500">
            Projects
          </p>

          <p className="text-3xl font-bold mt-2">
            {loading ? "..." : projects.length}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500">
            AI Tools
          </p>

          <p className="text-3xl font-bold mt-2">
            5
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-500">
            AI Provider
          </p>

          <p className="text-3xl font-bold mt-2">
            Ollama
          </p>
        </div>

      </div>

      {/* Quick Actions */}

      <div className="bg-white rounded-lg shadow p-6 mb-8">

        <h2 className="text-2xl font-semibold mb-4">
          Quick Actions
        </h2>

        <div className="flex flex-wrap gap-4">

          <Link
            to="/projects"
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded"
          >
            View Projects
          </Link>

          <Link
            to="/ai"
            className="bg-gray-800 hover:bg-gray-900 text-white px-5 py-3 rounded"
          >
            AI Assistant
          </Link>

        </div>

      </div>

      {/* Recent Projects */}

      <div>

        <h2 className="text-2xl font-semibold mb-4">
          Recent Projects
        </h2>

        {loading ? (
          <p className="text-gray-500">
            Loading projects...
          </p>
        ) : recentProjects.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-500">
              No projects yet.
            </p>

            <Link
              to="/projects"
              className="inline-block mt-4 text-blue-600 hover:underline"
            >
              Create your first project →
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">

            {recentProjects.map((project) => (
              <div
                key={project.id}
                className="bg-white rounded-lg shadow p-6"
              >
                <h3 className="text-xl font-semibold">
                  {project.name}
                </h3>

                <p className="text-gray-600 mt-2">
                  {project.description ||
                    "No description provided."}
                </p>

                <p className="text-sm text-gray-400 mt-4">
                  Created{" "}
                  {new Date(
                    project.created_at
                  ).toLocaleString()}
                </p>
              </div>
            ))}

          </div>
        )}

      </div>

    </div>
  );
}
