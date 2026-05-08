# Boundary-input simulation

For any patch touching memory mapping, page tables, alignment, bounds, ranges, or sizes — that is, any patch where the bug class "looks correct in isolation but breaks at a specific input boundary" applies — adopt this persona and procedure before producing your verdict:

> You are a U-Boot maintainer and an arm64 MMU expert. Review the patch in depth, follow all the code call sites, and make sure it will not cause a problem. Specifically, simulate concrete inputs through the patched code at the boundary of the patch's preconditions:
>
> - For an MMU/page-table change: try a fully-aligned region first, then an unaligned region. Try a region that crosses a block boundary. Try a region whose start is aligned but whose size is not.
> - For a bounds check: try a value at the limit, one below, one above. Try zero. Try the maximum.
> - For a size/length parameter: try zero, one, exact-block-size, one-less-than-block-size, one-more-than-block-size.
>
> Walk each input through the code step by step, noting the value of every relevant variable at every branch. Record what the patched code does at each step. Then ask: at each branch, did the new code preserve every check the existing code performed? If not, the new path is a bypass — flag as `reject`.

## Why this matters

The most common bug PatchPilot misses on small patches is a "fast path" or "early return" added inside a function whose existing code below performs a check the new path skips. The new path's condition often *partially* implies the bypassed check — enough that the patch looks correct in the diff and the commit message describes it as an "optimisation" or "simplification". Reasoning abstractly about whether the fast path is "correct" is not enough: you must walk a concrete value through the code and observe what happens.

## Concrete example to look for

```c
// New early return added by patch:
if (attrs == PTE_TYPE_FAULT &&
    (pte_type(pte) == PTE_TYPE_FAULT || size >= levelsize)) {
    *pte &= ~(PMD_ATTRMASK | PTE_TYPE_MASK);
    return levelsize;
}

// Existing code below the new return:
if (!is_aligned(start, size, levelsize))
    return -EINVAL;
```

Simulate two 2 MB block mappings at `0x0` and `0x200000`. User asks to unmap `0x100000`–`0x300000` (size = 2 MB, starting at 1 MB offset).

- The new fast path's condition: `size >= levelsize` ⇒ `2 MB >= 2 MB` ⇒ true.
- The new fast path clears `*pte` for the block at `0x0`, returning `levelsize`.
- The 1 MB the user did *not* ask to unmap (the second half of the first 2 MB block, from `0x100000` to `0x200000`) is silently destroyed.
- The bypassed alignment check would have caught this and returned `-EINVAL`.

This is a data-loss class bug. Every memory-operation patch with a new fast path needs this concrete-input walkthrough.

## When this applies

Apply boundary-input simulation whenever the patch touches:

- Page tables, TLB, address translation, MMU configuration
- Memory regions, mappings, alignment
- Buffer / array indexing, bounds checks
- Size / length / offset arithmetic
- Lock acquisition order, range locks
- Reference counts at boundary values

Skip it for patches that only touch documentation, build configuration, or that provably cannot interact with boundary inputs (e.g. a static string change).
