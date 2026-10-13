class FiniteStateMachine:
    """
    Автомат состояний для контроля логики LLM-агента.
    """
    def __init__(self, transitions_list: list[list[str]], default_state: str):
        # Делаем копию данных, чтобы не менять внешние переменные
        self.transitions = [list(pair) for pair in transitions_list]
        
        # Получаем уникальные состояния
        self.states = list(set([state for pair in self.transitions for state in pair]))
        
        if default_state not in self.states:
            raise ValueError(
                f"Default state '{default_state}' is not in states: {self.states}"
            )
            
        self.current_state = default_state

    def transition(self, new_state: str) -> str:
        """Переводит агента в новое состояние, если шаг валиден."""
        if [self.current_state, new_state] in self.transitions:
            self.current_state = new_state
            return self.current_state
        
        raise ValueError(
            f"Invalid transition for Agent from '{self.current_state}' to '{new_state}'. "
            f"Allowed transitions from current state: {self.get_allowed_transitions()}"
        )

    def get_allowed_transitions(self) -> list[str]:
        """Возвращает список состояний, куда агент может шагнут прямо сейчас."""
        return [target for source, target in self.transitions if source == self.current_state]

    def get_schema(self) -> dict:
        return {
            "current_state": self.current_state,
            "allowed_next_states": self.get_allowed_transitions(),
            "all_states": self.states,
            "all_transitions": self.transitions
        }