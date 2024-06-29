import { useState, useEffect } from 'react';
import axios from 'axios';

interface FetchData<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

const useFetch = <T, >(url: string): FetchData<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get<T>(url);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, [url]);

  return { data, loading, error };
};

export default useFetch;
