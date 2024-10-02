import gymnasium as gym
import numpy as np
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Optional, Dict, Any


class TradeEnv(gym.Env, ABC):
    """
    A custom OpenAI Gym environment for simulating trading actions within a spot market.

    This environment facilitates the simulation of trading strategies by managing 
    an account's balance, executing buy/sell actions, and tracking the history of 
    assets and trades. It interfaces with a data feeder to receive market data and 
    utilizes an account management system to handle transactions and account state.

    Attributes:
        _feeder (object): An instance that provides market data and manages the data feed.
        _account (Callable): A callable that initializes and manages the trading account.
        _action (Enum): An enumeration of possible trading actions (e.g., BUY, SELL, HOLD).
        _balance (int): The initial cash balance available for trading.
        _buy_quantity (int): The default quantity of assets to buy per transaction.
        _fee (float): The transaction fee percentage applied to each trade.
        _tax (float): The transaction tax percentage applied to each sale.
        action_space (gym.spaces.Discrete): The space of possible actions defined by the Action enum.
        observation_space (gym.spaces.Box): The space representing the shape and type of observations.
    """

    def __init__(
        self, 
        feeder: object, 
        account: Callable = None, 
        action: Enum = None, 
        balance: int = 1_000_000, 
        buy_quantity: int = 10, 
        fee: float = 0.3, 
        tax: float = 0.38
    ):
        """
        Initializes the TradeEnv environment with the specified parameters.

        Args:
            feeder (object): An instance that provides market data and manages the data feed.
            account (Callable, optional): A callable that initializes and manages the trading account. 
                Defaults to None.
            action (Enum, optional): An enumeration of possible trading actions (e.g., BUY, SELL, HOLD). 
                Defaults to None.
            balance (int, optional): The initial cash balance available for trading. 
                Defaults to 1,000,000.
            buy_quantity (int, optional): The default quantity of assets to buy per transaction. 
                Defaults to 10.
            fee (float, optional): The transaction fee percentage applied to each trade. 
                Defaults to 0.3.
            tax (float, optional): The transaction tax percentage applied to each sale. 
                Defaults to 0.38.
        """
        super(TradeEnv, self).__init__()
        
        self._feeder = feeder
        self._account_class = account
        self._account = None
        self._action = action
        self._balance = balance
        self._buy_quantity = buy_quantity
        self._fee = fee
        self._tax = tax
        
        # Define the action space based on the number of possible actions
        self.action_space = gym.spaces.Discrete(len(action))
        
        # Define the observation space with appropriate shape and data type
        self.observation_space = gym.spaces.Box(
            low=-np.inf, 
            high=np.inf, 
            shape=self._feeder.partShape(), 
            dtype=np.float32
        )

    def history(self):
        """
        Retrieves the historical records of account assets and trades.

        Returns:
            tuple: A tuple containing two DataFrames:
                - asset: The asset history DataFrame.
                - trade: The trade history DataFrame.
        """
        return self._account.getHistory()
    
    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None):
        """
        Resets the environment to an initial state and returns the initial observation.

        This method resets the data feeder, initializes a new trading account with 
        default parameters, retrieves the first set of market data, and records 
        the initial state of the account.

        Returns:
            tuple: A tuple containing the initial observations and additional info:
                - obs (np.ndarray): The initial observation array.
                - extra_info (dict): A dictionary containing extra information such as 
                  feed changes, asset history, and trade history.
        """
        super().reset(seed=seed)

        if seed is not None:
            np.random.seed(seed)
        
        self._feeder.reset()
        feed_info = self._feeder.info()
        self._account = self._account_class(
            feed_info["code"],
            feed_info["name"],
            balance=self._balance,
            fee=self._fee,
            tax=self._tax
        )
        
        self._obs, self._feed_change = self._feeder.next()
        self._account.hold(
            self._obs[0][self._feeder.col_daytime()],
            self._obs[0][self._feeder.col_price()]
        )
        return self._obs, self._extra_infos(self._obs)
    
    def _extra_infos(self, obs):
        """
        Generates additional information about the current state of the environment.

        This includes checking if trading is possible based on the current balance and 
        asset quantity, and packaging asset and trade histories.

        Args:
            obs (np.ndarray): The current observation array.

        Returns:
            dict: A dictionary containing:
                - "feed_change" (object): Information about changes in the data feed.
                - "asset" (object or None): The latest asset history record, if available.
                - "trade" (object or None): The latest trade history record, if available.
        """
        hist_asset, hist_trade = self.history()
        self._cant_trade = False
        if (
            hist_asset[0].balance < obs[0][self._feeder.col_price()] 
            and hist_asset[0].quantity == 0
        ):
            self._cant_trade = True
        return {
            "feed_change": self._feed_change,
            "asset": hist_asset[0] if len(hist_asset) > 0 else None,
            "trade": hist_trade[0] if len(hist_trade) > 0 else None,
        }
    
    def _terminated(self, obs, feed_change):
        """
        Determines whether the episode has terminated.

        The episode is considered terminated if both the observation and feed change 
        are None.

        Args:
            obs (np.ndarray or None): The current observation array.
            feed_change (object or None): Information about changes in the data feed.

        Returns:
            bool: True if the episode is terminated, False otherwise.
        """
        if obs is None and feed_change is None:
            return True

        return False
    
    def _truncated(self, obs, feed_change):
        """
        Determines whether the episode has been truncated.

        The episode is considered truncated if trading is not possible based on 
        the current account balance and asset quantity.

        Args:
            obs (np.ndarray or None): The current observation array.
            feed_change (object or None): Information about changes in the data feed.

        Returns:
            bool: True if the episode is truncated, False otherwise.
        """
        return self._cant_trade

    @abstractmethod
    def _act(self, action, rate, obs, feed_change):
        """
        Executes the specified action within the environment.

        This abstract method must be implemented by subclasses to define how 
        actions affect the environment's state.

        Args:
            action (int): The action to be taken, corresponding to the action space.
            rate (float): An additional parameter that may influence the action.
            obs (np.ndarray): The current observation array.
            feed_change (object): Information about changes in the data feed.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        pass
    
    @abstractmethod
    def _reward(self, action, rate, obs, feed_change, asset, trade):
        """
        Calculates the reward for the given action and state.

        This abstract method must be implemented by subclasses to define how 
        rewards are calculated based on actions and state transitions.

        Args:
            action (int): The action taken.
            rate (float): An additional parameter that may influence the reward.
            obs (np.ndarray): The current observation array after the action.
            feed_change (object): Information about changes in the data feed after the action.
            asset (object or None): The latest asset history record.
            trade (object or None): The latest trade history record.

        Returns:
            float: The calculated reward for the action and state.
        """
        return 0
    
    def step(self, action, rate=0):
        """
        Executes one time step within the environment based on the given action.

        This method processes the action, updates the environment's state, 
        calculates the reward, and determines if the episode has terminated 
        or been truncated.

        Args:
            action (int): The action to take, corresponding to the action space.
            rate (float, optional): An additional parameter that may influence the action. 
                Defaults to 0.

        Returns:
            tuple: A tuple containing:
                - obs (np.ndarray): The next observation array.
                - reward (float): The reward obtained from taking the action.
                - terminated (bool): Whether the episode has terminated.
                - truncated (bool): Whether the episode has been truncated.
                - extra_info (dict): Additional information about the environment's state.
        """
        terminated = self._terminated(self._obs, self._feed_change)
        truncated = self._truncated(self._obs, self._feed_change)

        # Execute the action
        act = self._act(action, rate, self._obs, self._feed_change)
        
        # Get the next set of observations from the feeder
        self._obs, self._feed_change = self._feeder.next()
        
        # Gather additional information
        extra_info = self._extra_infos(self._obs)
        
        # Calculate the reward based on the action and new state
        reward = self._reward(
            action, rate, self._obs, self._feed_change, 
            extra_info["asset"], extra_info["trade"]
        )

        return self._obs, reward, terminated, truncated, extra_info
