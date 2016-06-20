using System;

public static class RandomizedIndexManager
{
    
	public static int[] getLocationOrderIndices(int userId, int experimentId)
    {
        return locationOrders[(4 * experimentId + userId) % 12];
    }
    public static int[][] getTurnToFaceRandomizationIndices(int userId, int experimentId)
    {
        return randomizationIndices[(userId + experimentId) % 12];
    }

    private static int[][] locationOrders = new int[12][] {
        new int[6]{3, 4, 5, 1, 0, 2},
        new int[6]{0, 4, 2, 5, 1, 3},
        new int[6]{3, 0, 5, 4, 1, 2},
        new int[6]{0, 1, 3, 5, 2, 4},
        new int[6]{0, 5, 1, 3, 2, 4},
        new int[6]{1, 3, 2, 0, 5, 4},
        new int[6]{0, 2, 5, 3, 4, 1},
        new int[6]{1, 0, 3, 2, 4, 5},
        new int[6]{1, 4, 2, 0, 5, 3},
        new int[6]{3, 1, 5, 4, 0, 2},
        new int[6]{0, 4, 5, 3, 1, 2},
        new int[6]{1, 2, 3, 0, 5, 4}
    };

    // for twelve participants, have array[6] of arrays[3] of indices of objects to look at
    private static int[][][] randomizationIndices = new int[12][][]{
        new int[6][]{new int[3]{1, 0, 2}, new int[3]{2, 0, 1}, new int[3]{2, 0, 1}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}, new int[3]{2, 1, 0}},
        new int[6][]{new int[3]{2, 1, 0}, new int[3]{2, 0, 1}, new int[3]{0, 1, 2}, new int[3]{0, 1, 2}, new int[3]{1, 2, 0}, new int[3]{2, 1, 0}},
        new int[6][]{new int[3]{1, 0, 2}, new int[3]{1, 0, 2}, new int[3]{1, 0, 2}, new int[3]{1, 0, 2}, new int[3]{0, 2, 1}, new int[3]{2, 0, 1}},
        new int[6][]{new int[3]{0, 1, 2}, new int[3]{1, 0, 2}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}, new int[3]{1, 2, 0}, new int[3]{1, 0, 2}},
        new int[6][]{new int[3]{0, 1, 2}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}, new int[3]{0, 1, 2}, new int[3]{2, 1, 0}, new int[3]{2, 0, 1}},
        new int[6][]{new int[3]{2, 0, 1}, new int[3]{0, 2, 1}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}},
        new int[6][]{new int[3]{1, 0, 2}, new int[3]{1, 2, 0}, new int[3]{2, 1, 0}, new int[3]{1, 0, 2}, new int[3]{1, 2, 0}, new int[3]{0, 1, 2}},
        new int[6][]{new int[3]{0, 1, 2}, new int[3]{1, 0, 2}, new int[3]{2, 0, 1}, new int[3]{1, 0, 2}, new int[3]{2, 0, 1}, new int[3]{1, 2, 0}},
        new int[6][]{new int[3]{2, 0, 1}, new int[3]{0, 2, 1}, new int[3]{2, 1, 0}, new int[3]{1, 2, 0}, new int[3]{1, 2, 0}, new int[3]{1, 0, 2}},
        new int[6][]{new int[3]{0, 1, 2}, new int[3]{2, 0, 1}, new int[3]{2, 1, 0}, new int[3]{0, 1, 2}, new int[3]{1, 2, 0}, new int[3]{2, 1, 0}},
        new int[6][]{new int[3]{2, 1, 0}, new int[3]{2, 1, 0}, new int[3]{2, 0, 1}, new int[3]{0, 2, 1}, new int[3]{0, 1, 2}, new int[3]{2, 1, 0}},
        new int[6][]{new int[3]{2, 0, 1}, new int[3]{0, 1, 2}, new int[3]{1, 2, 0}, new int[3]{0, 2, 1}, new int[3]{1, 2, 0}, new int[3]{2, 1, 0}}
    };
}
