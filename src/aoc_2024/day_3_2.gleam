import gleam/int
import gleam/list
import gleam/option.{Some}
import gleam/regexp

pub opaque type Tok {
  Num(Int)
  Start
  Stop
}

pub fn parse(input: String) -> List(Tok) {
  let opts = regexp.Options(case_insensitive: False, multi_line: True)
  let assert Ok(p) =
    regexp.compile("don't\\(\\)|do\\(\\)|mul\\((\\d{1,3}),(\\d{1,3})\\)", opts)
  let matches = regexp.scan(input, with: p)
  use match <- list.map(matches)
  case match {
    regexp.Match("do()", _) -> Start
    regexp.Match("don't()", _) -> Stop
    _ -> {
      let assert [Some(n1), Some(n2)] = match.submatches
      let assert Ok(n1) = int.parse(n1)
      let assert Ok(n2) = int.parse(n2)
      Num(n1 * n2)
    }
  }
}

pub fn pt_1(input: List(Tok)) {
  use acc, x <- list.fold(input, 0)
  case x {
    Num(x) -> acc + x
    _ -> acc
  }
}

pub fn pt_2(input: List(Tok)) {
  {
    use #(acc, enabled), token <- list.fold(input, #(0, True))
    case token {
      Start -> #(acc, True)
      Stop -> #(acc, False)
      Num(x) if enabled -> #(acc + x, enabled)
      Num(_) -> #(acc, enabled)
    }
  }.0
}
