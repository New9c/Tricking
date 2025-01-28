import '../styles/global.scss';
import React, { useEffect, useState } from "react";
import '../styles/tricktionary.scss';
import Topbar from "./Topbar";
import Loading from "./Loading";
import ErrorPage from './Error';

interface TrickData {
  [level: string]: {
    [name: string]: (string)
  };
}

const Tricktionary: React.FC = () => {
  const [tricks, setTricks] = useState<TrickData | null>(null); // null indicates data is not loaded
  const [isLoading, setIsLoading] = useState(true); // Tracks loading state
  const [error, setError] = useState<string | null>(null); // Tracks errors

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
  useEffect(() => {
    fetchTricks();
  }, []);

  if (isLoading) {
    return <Loading />
  }

  if (error) {
    return <ErrorPage />;
  }

  return (
    <>
      <Topbar />
      <div>
        {
          tricks &&
          Object.entries(tricks).map(([level, tricksAtLevel]) => (
            <div key={level}>
              <header>{level.charAt(0).toUpperCase() + level.slice(1)}</header>
              <div className="multiple-tricks">
                {Object.entries(tricksAtLevel).map(([name, desc]) => (
                  <button
                    className="trick-btn"
                    key={name}
                    title={desc}
                  >
                    {name}
                  </button>
                ))}
              </div>
            </div>
          ))};
      </div>
    </>
  );
};

export default Tricktionary;
