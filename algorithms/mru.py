"""
MRU (Most Recently Used) Page Replacement Algorithm
-----------------------------------------------------
Replaces the page that has been used most recently.
This is the inverse of LRU — it evicts the page at the top of the recency stack.

Reference:
    Tanenbaum, A. S., & Bos, H. (2014).
    Modern Operating Systems (4th ed.). Pearson.
    Chapter 3: Memory Management, p. 213.
"""

from collections import OrderedDict


def simulate(reference_string: list, num_frames: int) -> dict:
    """
    Simulate the MRU page replacement algorithm.

    Args:
        reference_string: List of page numbers to reference.
        num_frames: Number of available page frames.

    Returns:
        A dict with simulation results including frame history and statistics.
    """
    frames = OrderedDict()    # key=page; order = LRU at left, MRU at right
    frames_history = []
    fault_flags = []
    evicted_pages = []

    for page in reference_string:
        is_fault = page not in frames
        evicted = None

        if is_fault:
            if len(frames) >= num_frames:
                # Evict the most recently used page (last in OrderedDict)
                evicted, _ = frames.popitem(last=True)
            frames[page] = None
        else:
            # Move accessed page to the MRU end so it becomes the eviction candidate
            frames.move_to_end(page, last=True)

        fault_flags.append(is_fault)
        evicted_pages.append(evicted)
        pages_in_frames = list(frames.keys())
        frames_history.append(pages_in_frames + [None] * (num_frames - len(pages_in_frames)))

    total_faults = sum(fault_flags)
    total_hits = len(reference_string) - total_faults
    total = len(reference_string)

    return {
        "algorithm": "MRU",
        "reference_string": reference_string,
        "num_frames": num_frames,
        "frames_history": frames_history,
        "fault_flags": fault_flags,
        "evicted_pages": evicted_pages,
        "total_faults": total_faults,
        "total_hits": total_hits,
        "fault_rate": round(total_faults / total * 100, 2) if total > 0 else 0.0,
        "hit_rate": round(total_hits / total * 100, 2) if total > 0 else 0.0,
    }
