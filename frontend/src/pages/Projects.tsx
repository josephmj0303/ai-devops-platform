import { useEffect, useState } from "react";

import {
  createProject,
  getProjects,
} from "../api/projects";

import type {
  Project,
} from "../types/project";

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const loadProjects = async () => {
    try {
      setError("");

      const data = await getProjects();

      setProjects(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load projects.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreateProject = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    if (!name.trim()) {
      setError("Project name is required.");
      return;
    }

    try {
      setCreating(true);
      setError("");

      const project = await createProject({
        name: name.trim(),
        description: description.trim() || undefined,
      });

      setProjects((current) => [
        ...current,
        project,
      ]);

      setName("");
      setDescription("");
    } catch (err) {
      console.error(err);
      setError("Failed to create project.");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">

      <div className="mb-8">
        <h1 className="text-4xl font-bold">
          Projects
        </h1>

        <p className="text-gray-600 mt-2">
          Manage your DevOps projects.
        </p>
      </div>

      {/* Create Project */}

      <div className="bg-white rounded-lg shadow p-6 mb-8">

        <h2 className="text-2xl font-semibold mb-4">
          Create Project
        </h2>

        <form onSubmit={handleCreateProject}>

          <input
            type="text"
            placeholder="Project name"
            value={name}
            onChange={(e) =>
              setName(e.target.value)
            }
            className="border w-full p-3 rounded mb-4"
          />

          <textarea
            placeholder="Project description (optional)"
            value={description}
            onChange={(e) =>
              setDescription(e.target.value)
            }
            className="border w-full p-3 rounded mb-4"
            rows={3}
          />

          {error && (
            <div className="text-red-500 mb-4">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={creating}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-3 rounded"
          >
            {creating
              ? "Creating..."
              : "Create Project"}
          </button>

        </form>
      </div>

      {/* Project List */}

      <div>

        <h2 className="text-2xl font-semibold mb-4">
          My Projects
        </h2>

        {loading ? (
          <p>Loading projects...</p>
        ) : projects.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-gray-500">
              No projects yet. Create your first project above.
            </p>
          </div>
        ) : (
          <div className="grid gap-4">

            {projects.map((project) => (
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

                <div className="text-sm text-gray-400 mt-4">
                  Created:{" "}
                  {new Date(
                    project.created_at
                  ).toLocaleString()}
                </div>

              </div>
            ))}

          </div>
        )}

      </div>

    </div>
  );
}
