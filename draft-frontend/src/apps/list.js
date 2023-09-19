import '../App.css';
import { useLocation } from "react-router-dom"
import { useEffect, useState } from 'react';
import { format } from 'react-string-format'

function PokemonList() {
    const [draft, setDraft] = useState([])
    const [pokemon, setPokemon] = useState([])

    const getDraft = async() => {
        const response = fetch(
            "http://localhost:8000/drafts_list/12/"
        );
        const json = (await response).json();
        return json;
    }

    useEffect(() => {
        getDraft().then(draft => {
            setDraft(draft);
        });
    }, []);

    return (
        <div className="draft">
            {
                draft.pokemon_list.map((item, i)  => (
                    <p>{item['name']}</p>
                ))
            }
            <div>
                <p>HI</p>
            </div>
        </div>
    );
}

export default PokemonList;