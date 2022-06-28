---
title: "Learning Julia, Line by Line"
author: "poga"
date: 2021-08-04
tags:
  - Notes
  - Programming
  - Julia
categories:
  - Blog
---

[Cardsjl](https://github.com/StefanKarpinski/Cards.jl) is a simple Julia package which demonstrate many interesting bits of the [Julia Programming Language](https://julialang.org/).

Reading it is an enjoyable experience. The note I've writtend down is here:

<!--more-->

```julia
# import base multiply(*), bitwise-or(|), and bitwise-and(&)
#
# In Julia, you can load modules with `using` or `import`. The difference is that
# * `using` will load the module **and** reexport the loaded module into the surrounding global
#    namespace.
# * `import` will only load the module and rexport the module name to the scope.
import Base: *, |, &


"""
Encode a suit as a 2-bit value (low bits of a `UInt8`):

- 0 = ♣ (clubs)
- 1 = ♢ (diamonds)
- 2 = ♡ (hearts)
- 3 = ♠ (spades)

The suits have global constant bindings: `♣`, `♢`, `♡`, `♠`.
"""
# Here we define a struct `Suit`. A `Suit` contains a `i` variable with type`UInt8`
#
# In Julia, type objects are constructor functions. We can create new instance of the struct
# via calling the function `suit = Suit(0)`
struct Suit
  i::UInt8

  # Here, we define an "Inner Constructor Method" to define constraints for the constructor
  #
  # This is also a neat example of Julia's unicode support. Yes, we can use ≤ as `<=`.
  Suit(s::Integer) = 0 ≤ s ≤ 3 ? new(s) :
  throw(ArgumentError("invalid suit number: $s"))
end

# Julia's abstraction is mostly powered by multiple dispatch.
# Here we define a "new dispatch" for `char()` function to convert normal characters to a Suit.
# Therefore, whenever the `char()` function is applied with a `Suit`, this dispatch will be used.
char(s::Suit) = Char(0x2663-s.i)
# ... and some other helpers. They're surprisingly self-explanatory
Base.string(s::Suit) = string(char(s))
Base.show(io::IO, s::Suit) = print(io, char(s))

# In a normal poker deck, there's only 4 possible suits
# We can write readable codes with the power of unicode symbols in Julia
const ♣ = Suit(0)
const ♢ = Suit(1)
const ♡ = Suit(2)
const ♠ = Suit(3)

const suits = [♣, ♢, ♡, ♠]

"""
Encode a playing card as a 6-bit integer (low bits of a `UInt8`):

- low bits represent rank from 0 to 15
- high bits represent suit (♣, ♢, ♡ or ♠)

Ranks are assigned as follows:

- numbered cards (2 to 10) have rank equal to their number
- jacks, queens and kings have ranks 11, 12 and 13
- there are low and high aces with ranks 1 and 14
- there are low and high jokers with ranks 0 and 15

This allows any of the standard orderings of cards ranks to be
achieved simply by choosing which aces or which jokers to use.
There are a total of 64 possible card values with this scheme,
represented by `UInt8` values `0x00` through `0x3f`.
"""
# A Card is a struct which encode the suit and the rank into a single UInt8
#
# In most high-level languages, this would be kinda tedious to define.
# However, Julia demonstrated its expressiveness straight to the lowest level here.
struct Card
  value::UInt8
end

# We create a new dispatch for `Card`'s constructor.
# It will encode the rank and the suit into the UInt8
function Card(r::Integer, s::Integer)
  0 ≤ r ≤ 15 || throw(ArgumentError("invalid card rank: $r"))
  return Card(((s << 4) % UInt8) | (r % UInt8))
end
# Another dispath when a suit is given instead of an integer for suit
Card(r::Integer, s::Suit) = Card(r, s.i)

# These are getters for getting the rank or suit from a card
suit(c::Card) = Suit((0x30 & c.value) >>> 4)
rank(c::Card) = (c.value & 0x0f) % Int8

# Lets define a new dispatch for Base.show to make it looks good when printed.
function Base.show(io::IO, c::Card)
  r = rank(c)
  if 1 ≤ r ≤ 14
    r == 10 && print(io, '1')
    print(io, "1234567890JQKA"[r])
  else
    print(io, '\U1f0cf')
  end
  print(io, suit(c))
end

# In Julia, `2 * x` can be written as `2x`.
#
# By creating a new dispatch for the multiply operator `*`, we can write `2♣`
# and it will automatically converted to `Card(2, ♣)`. WOW fancy.
*(r::Integer, s::Suit) = Card(r, s)

# However, "J♣" will not be treated as a multipication.
#
# Here we use `@eval` macro to create these variables as consts.
# such lispy. I like it.
for s in "♣♢♡♠", (r,f) in zip(11:14, "JQKA")
  ss, sc = Symbol(s), Symbol("$f$s")
  @eval (export $sc; const $sc = Card($r,$ss))
end

"""
Represent a hand (set) of cards using a `UInt64` bit set.
"""
# we use an `UInt64` bit set to store what cards are presented in a hand
# since there's only 52 cards in a deck.
#
# We use `<:` to indicate that a `Hand` is a subtype of a `AbstractSet{Card}`.
# Therefore, `Hand` can be used with all functions with compatiable dispatch to an `AbstractSet`.
struct Hand <: AbstractSet{Card}
  cards::UInt64
  Hand(cards::UInt64) = new(cards)
end

# convert card value to bit	set position
bit(c::Card) = one(UInt64) << c.value
# convert suit to bit set range
bits(s::Suit) = UInt64(0xffff) << 16(s.i)

# a simple constructor to convert a set of cards to a bit set
function Hand(cards)
  hand = Hand(zero(UInt64))
  for card in cards
    card isa Card || throw(ArgumentError("not a card: $repr(card)"))
    i = bit(card)
    hand.cards & i == 0 || throw(ArgumentError("duplicate cards are not supported"))
    hand = Hand(hand.cards | i)
  end
  return hand
end

# Some more dispatches for our Hand type
Base.in(c::Card, h::Hand) = (bit(c) & h.cards) != 0
Base.length(h::Hand) = count_ones(h.cards)
Base.isempty(h::Hand) = h.cards == 0
Base.lastindex(h::Hand) = length(h)

# Define an iterator for our Hand.
#
# We can define a parameter with default value with the syntax introduced here
function Base.iterate(h::Hand, s::UInt8 = trailing_zeros(h.cards) % UInt8)
  (h.cards >>> s) == 0 && return nothing
  c = Card(s); s += true
  c, s + trailing_zeros(h.cards >>> s) % UInt8
end

# a non-bound-checked function to get a Card from a Hand
function Base.unsafe_getindex(h::Hand, i::UInt8)
  card, s = 0x0, 0x5
  while true
    mask = 0xffff_ffff_ffff_ffff >> (0x40 - (0x1<<s) - card)
    card += UInt8(i > count_ones(h.cards & mask) % UInt8) << s
    s > 0 || break
    s -= 0x1
  end
  return Card(card)
end

# To avoid having to convert from UInt8 to Integer constantly,
# we create a new dispatch for our unsafe_getindex for all Integeres
Base.unsafe_getindex(h::Hand, i::Integer) = Base.unsafe_getindex(h, i % UInt8)

# Finally, we wrap our not-so-safe fuction with a bounded-checked `getindex` function
function Base.getindex(h::Hand, i::Integer)
  # The `@boundscheck` macro allows the bound check to be ignored with `@inbound` macro
  @boundscheck 1 ≤ i ≤ length(h) || throw(BoundsError(h,i))
  return Base.unsafe_getindex(h, i)
end

# Make a `Hand` looks nice when printed
function Base.show(io::IO, hand::Hand)
  if isempty(hand) || !get(io, :compact, false)
    print(io, "Hand([")
    for card in hand
      print(io, card)
      (bit(card) << 1) ≤ hand.cards && print(io, ", ")
    end
    print(io, "])")
  else
    for suit in suits
      s = hand & suit
      isempty(s) && continue
      show(io, suit)
      for card in s
        r = rank(card)
        if r == 10
          print(io, '\u2491')
        elseif 1 ≤ r ≤ 14
          print(io, "1234567890JQKA"[r])
        else
          print(io, '\U1f0cf')
        end
      end
    end
  end
end

# More dispatch to allow us to combine two hands with `|`, add a card to a hand with `|`
a::Hand | b::Hand = Hand(a.cards | b.cards)
a::Hand | c::Card = Hand(a.cards | bit(c))
c::Card | h::Hand = h | c

# interset two hands with `&`
a::Hand & b::Hand = Hand(a.cards & b.cards)
# fetch cards within a suit range with `&`
h::Hand & s::Suit = Hand(h.cards & bits(s))
s::Suit & h::Hand = h & s

# more new dispatches
Base.intersect(s::Suit, h::Hand) = h & s
Base.intersect(h::Hand, s::Suit) = intersect(s::Suit, h::Hand)

# range operators for our suit and cards
*(rr::OrdinalRange{<:Integer}, s::Suit) = Hand(Card(r,s) for r in rr)
  ..(r::Integer, c::Card) = (r:rank(c))*suit(c)
  ..(a::Card, b::Card) = suit(a) == suit(b) ? rank(a)..b :
  throw(ArgumentError("card ranges need matching suits: $a vs $b"))

# FINALLY, we create a deck, which contains 52 unique cards
const deck = Hand(Card(r,s) for s in suits for r = 2:14)

# An empty hand can be represented as 0
Base.empty(::Type{Hand}) = Hand(zero(UInt64))

# Use `rand` to get a random subset of the deck
# we use @eval to interpolate all cards into this expression then evaluate it
@eval Base.rand(::Type{Hand}) = Hand($(deck.cards) & rand(UInt64))

# In Julia, a function ends with `!` indicates that it's an in-place update function
#
# Here we define a `deal!` function to fill hands based on specified `counts` layout
function deal!(counts::Vector{<:Integer}, hands::AbstractArray{Hand}, offset::Int=0)
  for rank = 2:14, suit = 0:3
    while true
      hand = rand(1:4)
      if counts[hand] > 0
        counts[hand] -= 1
        hands[offset + hand] |= Card(rank, suit)
        break
      end
    end
  end
  return hands
end

# Now let's define our `deal` function. It will deal cards to 4 people with the given count
#
# Default dispatch when no argument provided
deal() = deal!(fill(13, 4), fill(empty(Hand), 4))

# a dispatch for `deal` when an `n` Int is provided
function deal(n::Int)
  counts = fill(0x0, 4)
  hands = fill(empty(Hand), 4, n)
  for i = 1:n
    deal!(fill!(counts, 13), hands, 4(i-1))
  end
  return permutedims(hands)
end

# calculate the points of a given hand
function points(hand::Hand)
  p = 0
  for rank = 11:14, suit = 0:3
    card = Card(rank, suit)
    p += (rank-10)*(card in hand)
  end
  return p
end
```
