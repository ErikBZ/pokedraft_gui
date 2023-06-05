import '../App.css';
import { useLocation } from "react-router-dom"
import { useEffect, useState } from 'react';

function List() {
    const [draft, setDraft] = useState([])
    const location = useLocation();

    const getDraft = async() => {
        const response = fetch(
            "http://localhost:8000/drafts/4"
        );
        const json = (await response).json();
        return json;
    }

    useEffect(() => {
        getDraft().then(draft => {
            setDraft(draft)
        });
    }, []);

    return (
        <div className="draft">
            {
                draft["pokemon_list"].map((item, i) => (
                    <p>{item}</p>
                ))
            }
        </div>
    );
}

export default List;