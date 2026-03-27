"""
LRU (Least Recently Used) Page Replacement Algorithm
------------------------------------------------------
Replaces the page that has not been used for the longest period of time.
Tracks the recency of each page access using an ordered dictionary.

Reference:
    Silberschatz, A., Galvin, P. B., & Gagne, G. (2018).
    Operating System Concepts (10th ed.). Wiley.
    Chapter 10: Virtual Memory, pp. 440-443.
"""

from collections import OrderedDict


def simulate(reference_string: list, num_frames: int) -> dict:
    """
    Simulate the LRU page replacement algorithm.

    Args:
        reference_string: List of page numbers to reference.
        num_frames: Number of available page frames.

    Returns:
        A dict with simulation results including frame history and statistics.
    """
    frames = OrderedDict()    # key=page, value=None; order = LRU to MRU (left=oldest)
    frames_history = []
    fault_flags = []
    evicted_pages = []

    for page in reference_string:
        is_fault = page not in frames
        evicted = None

        if is_fault:
            if len(frames) >= num_frames:
                # Evict the least recently used page (first in OrderedDict)
                evicted, _ = frames.popitem(last=False)
            frames[page] = None
        else:
            # Move accessed page to the most-recently-used end
            frames.move_to_end(page, last=True)

        fault_flags.append(is_fault)
        evicted_pages.append(evicted)
        pages_in_frames = list(frames.keys())
        # Pad to num_frames with None
        frames_history.append(pages_in_frames + [None] * (num_frames - len(pages_in_frames)))

    total_faults = sum(fault_flags)
    total_hits = len(reference_string) - total_faults
    total = len(reference_string)

    return {
        "algorithm": "LRU",
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
