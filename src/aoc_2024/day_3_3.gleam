import gleam/int
import gleam/string
import party.{type Parser, do}

pub type State =
  #(Int, Bool)

fn p_mul() -> Parser(fn(State) -> #(Nil, State), e) {
  use _ <- do(party.string("mul("))
  use x <- do(party.digits())
  use _ <- do(party.char(","))
  use y <- do(party.digits())
  use _ <- do(party.char(")"))
  let assert Ok(x) = int.parse(x)
  let assert Ok(y) = int.parse(y)
  party.return(fn(state) {
    let #(acc, enabled) = state
    case enabled {
      True -> #(Nil, #(acc + x * y, enabled))
      False -> #(Nil, state)
    }
  })
}

fn p_do() -> Parser(fn(State) -> #(Nil, State), e) {
  use _ <- do(party.string("do()"))
  party.return(fn(state: State) { #(Nil, #(state.0, True)) })
}

fn p_dont() -> Parser(fn(State) -> #(Nil, State), e) {
  use _ <- do(party.string("don't()"))
  party.return(fn(state: State) { #(Nil, #(state.0, False)) })
}

fn p_ignore() -> Parser(fn(State) -> #(Nil, State), e) {
  use _ <- do(party.any_char())
  party.return(fn(state) { #(Nil, state) })
}

fn parser() {
  party.stateful_many(
    #(0, True),
    party.choice([p_mul(), p_do(), p_dont(), p_ignore()]),
  )
}

pub fn pt_1(input: String) {
  let assert Ok(res) = party.go(parser(), string.replace(input, "do", ""))
  res.1.0
}

pub fn pt_2(input: String) {
  let assert Ok(res) = party.go(parser(), input)
  res.1.0
}
