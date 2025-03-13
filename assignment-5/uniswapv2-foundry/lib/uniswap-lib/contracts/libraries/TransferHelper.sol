// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

library TransferHelper {
    function safeTransfer(
        address token,
        address to,
        uint value
    ) internal {
        (bool success, bytes memory data) = token.call(
            abi.encodeWithSelector(0xa9059cbb, to, value) // ERC20 transfer function
        );
        require(success && (data.length == 0 || abi.decode(data, (bool))), 'TransferHelper::safeTransfer: TRANSFER_FAILED');
    }

    // Add other necessary functions (safeTransferFrom, etc.) if needed
}