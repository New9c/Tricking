import React, { useEffect, useState } from "react";
import '../styles/tricktionary.scss';
import '../styles/global.scss';
import Topbar from "./Topbar";

interface TrickData {
  [level: string]: string[];
}
function goToTrickManager() {
  window.location.href = '/trick_manager';
}

const Tricktionary: React.FC = () => {
  const [tricks, setTricks] = useState<TrickData | null>(null); // null indicates data is not loaded
  const [isLoading, setIsLoading] = useState(true); // Tracks loading state
  const [error, setError] = useState<string | null>(null); // Tracks errors

  useEffect(() => {
    const fetchTricks = async () => {
      try {
        setIsLoading(true);
        const response = await fetch("http://localhost:8000/api/v1/tricktionary/get");
        if (!response.ok) {
          throw new Error("Failed to fetch tricks");
        }
        const data = await response.json();
        setTricks(data);
      } catch (err: any) {
        setError(err.message || "An unexpected error occurred");
      } finally {
        setIsLoading(false); // Loading finished
      }
    };

    fetchTricks();
  }, []);

  if (isLoading) {
    return <div>Loading tricks...</div>; // Loading indicator
  }

  if (error) {
    return <div>Error: {error}</div>; // Error message
  }

  return (
    <>
      <Topbar />
      <div className="add_delete_container">
        <button
          className="add_delete"
          onClick={goToTrickManager}>
          Add/Delete Tricks
        </button>
      </div>
      <div>
        {tricks &&
          Object.entries(tricks).map(([level, names]) => (
            <div key={level}>
              <header>{level.charAt(0).toUpperCase() + level.slice(1)}</header>
              <div className="multiple-tricks">
                {names.map((name) => (
                  <button
                    className="trick-btn"
                    key={name}>
                    {name}
                  </button>

                ))}
              </div>
            </div>
          ))}
      </div>
    </>
  );
};

export default Tricktionary;
