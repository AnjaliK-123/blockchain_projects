pragma solidity ^0.6.6;

import "forge-std/Test.sol";
import "lib/v2-core/contracts/interfaces/IUniswapV2ERC20.sol";
import "lib/v2-core/contracts/interfaces/IUniswapV2Factory.sol";
import "lib/v2-core/contracts/interfaces/IUniswapV2Pair.sol";
import "lib/v2-periphery/contracts/UniswapV2Router02.sol";
import "lib/uniswap-lib/contracts/libraries/TransferHelper.sol";
import "lib/uniswap-lib/contracts/libraries/FixedPoint.sol";
import "lib/uniswap-lib/contracts/libraries/Babylonian.sol";
import "lib/v2-core/contracts/UniswapV2Factory.sol";
import "lib/v2-core/contracts/UniswapV2Pair.sol";


contract UniswapV2Router02Test is Test {
    UniswapV2Router02 public router;
    UniswapV2Factory public factory;
    UniswapV2Pair public pair;
    UniswapV2ERC20 public tokenA;
    UniswapV2ERC20 public tokenB;


    function setUp() public {
        factory = new UniswapV2Factory();
        router = new UniswapV2Router02();

        tokenA = new UniswapV2ERC20();
        tokenB = new UniswapV2ERC20();


        tokenA._mint(address(tokenA), 1000 * 10**18);
        tokenB._mint(address(tokenB), 1000 * 10**18);

        factory.createPair(address(tokenA), address(tokenB));
        pair = UniswapV2Pair(factory.getPair(address(tokenA), address(tokenB)));
    }


    function testAddLiquidity() public {
        tokenA.approve(address(router), 500 * 10**18);
        tokenB.approve(address(router), 500 * 10**18);

        (uint amountA, uint amountB, uint liquidity) = router.addLiquidity(
            address(tokenA),
            address(tokenB),
            500 * 10**18,
            500 * 10**18,
            0,
            0,
            address(this),
            block.timestamp
        );

        assertEq(amountA, 500 * 10**18);
        assertEq(amountB, 500 * 10**18);
        assertGt(liquidity, 0);
    }

    function testSwapTokens() public {
        tokenA.approve(address(router), 500 * 10**18);
        tokenB.approve(address(router), 500 * 10**18);
        router.addLiquidity(address(tokenA), address(tokenB), 500 * 10**18, 500 * 10**18, 0, 0, address(this), block.timestamp);


        tokenA.approve(address(router), 100 * 10**18);
        address[] memory path = new address[][2];
        path[0] = address(tokenA);
        path[1] = address(tokenB);

        uint[] memory amounts = router.swapExactTokensForTokens(
            100 * 10**18,
            0, 
            path,
            address(this),
            block.timestamp
        );   

        assertGt(amounts[1], 0);     
    }

    function testRemoveLiquidity() public {
        tokenA.approve(address(router), 500 * 10**18);
        tokenB.approve(address(router), 500 * 10**18);
        router.addLiquidity(address(tokenA), address(tokenB), 500 * 10**18, 500 * 10**18, 0, 0, address(this), block.timestamp);

        uint liquidity = pair.balanceOf(address(this)); // Corrected from balanceof to balanceOf
        pair.approve(address(router), liquidity);

        (uint amountA, uint amountB) = router.removeLiquidity(
            address(tokenA),
            address(tokenB),
            liquidity,
            0,
            0,
            address(this),
            block.timestamp
        );

        assertGt(amountA, 0);
        assertGt(amountB, 0);
    }
}
