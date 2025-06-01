def aggregate_ner_results(ner_results, original_text=""):
    """
    Aggregate NER results using simple strategy (merge consecutive tokens with same entity).
    
    Args:
        ner_results: List of NER predictions from the model
        original_text: Original text (optional, used to extract words if needed)
    
    Returns:
        List of aggregated entities with format:
        [{'entity_group': str, 'score': float, 'word': str, 'start': int, 'end': int}, ...]
    """
    if not ner_results:
        return []
    
    aggregated = []
    current_group = None
    
    for token in ner_results:
        entity = token['entity']
        
        # Remove B- and I- prefixes to get the base entity type
        if entity.startswith(('B-', 'I-')):
            entity_type = entity[2:]
            prefix = entity[:2]
        else:
            entity_type = entity
            prefix = 'I-'  # Default to I- if no prefix
        
        # Start new group if:
        # 1. No current group
        # 2. Different entity type
        # 3. B- prefix (explicit beginning)
        # 4. Non-consecutive indices
        if (current_group is None or 
            current_group['entity_group'] != entity_type or 
            prefix == 'B-' or
            (current_group['tokens'] and token['index'] != current_group['tokens'][-1]['index'] + 1)):
            
            # Finalize previous group
            if current_group is not None:
                aggregated.append(_finalize_group(current_group, original_text))
            
            # Start new group
            current_group = {
                'entity_group': entity_type,
                'tokens': [token],
                'scores': [token['score']]
            }
        else:
            # Add to current group
            current_group['tokens'].append(token)
            current_group['scores'].append(token['score'])
    
    # Finalize last group
    if current_group is not None:
        aggregated.append(_finalize_group(current_group, original_text))
    
    return aggregated


def _finalize_group(group, original_text=""):
    """
    Convert a group of tokens into final aggregated entity.
    """
    tokens = group['tokens']
    scores = group['scores']
    
    # Calculate average score
    avg_score = sum(scores) / len(scores)
    
    # Get start and end positions
    start_pos = tokens[0]['start']
    end_pos = tokens[-1]['end']
    
    # Construct word by combining token words or extracting from original text
    if original_text:
        word = original_text[start_pos:end_pos]
    else:
        # Combine token words, handling special tokens like ▁
        word_parts = []
        for token in tokens:
            token_word = token['word']
            # Handle sentence piece tokens that start with ▁ (space indicator)
            if token_word.startswith('▁'):
                if word_parts:  # Add space if not the first token
                    word_parts.append(' ')
                word_parts.append(token_word[1:])  # Remove ▁
            else:
                word_parts.append(token_word)
        
        word = ''.join(word_parts).strip()
    
    return {
        'entity_group': group['entity_group'],
        'score': avg_score,
        'word': word,
        'start': start_pos,
        'end': end_pos
    }